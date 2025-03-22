from pprint import pprint as print
import os
import json
import re
import pandas as pd


def get_dicts_from_txt(file_path):
    namespace = {}
    # Read and execute the .txt file
    with open(file_path, 'r') as file:
        content = file.read()
    # Fix single quotes in strings containing apostrophes (replace them with double quotes)
        # Escape single quotes inside strings
    # content = re.sub(r"(['\"])(.*?)(\1)", lambda m: m.group(0).replace("'", "\"") if "'" in m.group(0) else m.group(0), content)
    # "\'s\s"g
    # handle possesives with 's
    content = re.sub(r"\'s\s", r' ', content)
    # handle won't
    content = re.sub(r"won\'t.\w+", r"will_not", content)
    exec(content, namespace)
    # Access the dictionaries from the namespace
    nsubj_verb_count_dict = namespace['nsubj_verb_count_dict']
    dobj_verb_count_dict = namespace['dobj_verb_count_dict']
    return nsubj_verb_count_dict, dobj_verb_count_dict


def load_sap_lexicon_as_dict(lexicon_path, dimension='power'):
    """
    Loads the SAP lexicon from a CSV file and returns it as a dictionary
    suitable for use with calculate_power_score.

    Args:
        lexicon_path (str): Path to the agency_power.csv file.
        dimension (str):  The dimension to load ('power' or 'agency').

    Returns:
        dict: A dictionary where keys are verbs and values are dictionaries
              containing 'agent' and 'theme' scores based on the 'power' or 'agency' dimension.
              Example: {'abandon': {'agent': 1, 'theme': -1}, 'abolish': {'agent': 1, 'theme': -1}, ...}
    """

    label_dict = {
        'power_agent': {'agent': 1, 'theme': -1},
        'power_theme': {'agent': -1, 'theme': 1},
        'power_equal': {'agent': 0, 'theme': 0},
        'agency_pos': {'agent': 1, 'theme': 0},
        'agency_neg': {'agent': -1, 'theme': 0},
        'agency_equal': {'agent': 0, 'theme': 0}
    }

    lexicon_df = pd.read_csv(lexicon_path)  # Removed `os.path.join(BASEPATH, ...)`
    verb_score_dict = {}

    for _, row in lexicon_df.iterrows():
        verb = row['verb'].strip()  # Directly access 'verb' column

        if dimension == 'power':
            label = row['power']  # Use 'power' column
        elif dimension == 'agency':
            label = row['agency']  # Use 'agency' column
        else:
            raise ValueError("Dimension must be 'power' or 'agency'")

        if pd.notna(label):  # Check for NaN/missing values
            verb_score_dict[verb] = label_dict[label]
        else:
            verb_score_dict[verb] = {'agent': 0, 'theme': 0} # handle empty values



    return verb_score_dict


def calculate_power_score(nsubj_verb_count_dict, dobj_verb_count_dict, verb_score_dict):
    """
    Calculates power scores for personas based on verb occurrences and a lexicon.

    Args:
        nsubj_verb_count_dict (dict): Counts of (persona, verb) where persona is the subject.
        dobj_verb_count_dict (dict): Counts of (persona, verb) where persona is the object.
        verb_score_dict (dict):  A dictionary of verbs and agent/theme power scores

    Returns:
        dict: A dictionary of personas and their calculated power scores.
    """

    # Create dataframes from the input dictionaries
    nsubj_df = pd.DataFrame.from_dict(nsubj_verb_count_dict, orient='index', columns=['count'])
    nsubj_df = nsubj_df.reset_index()
    nsubj_df[['persona', 'verb']] = pd.DataFrame(nsubj_df['index'].tolist(), index=nsubj_df.index)
    nsubj_df = nsubj_df.drop('index', axis=1)

    dobj_df = pd.DataFrame.from_dict(dobj_verb_count_dict, orient='index', columns=['count'])
    dobj_df = dobj_df.reset_index()
    dobj_df[['persona', 'verb']] = pd.DataFrame(dobj_df['index'].tolist(), index=dobj_df.index)
    dobj_df = dobj_df.drop('index', axis=1)


    # Add agent scores to nsubj_df and theme scores to dobj_df by merging with verb_score_dict
    nsubj_df['agent_score'] = nsubj_df['verb'].apply(lambda verb: verb_score_dict.get(verb, {}).get('agent', 0))
    dobj_df['theme_score'] = dobj_df['verb'].apply(lambda verb: verb_score_dict.get(verb, {}).get('theme', 0))


    # Calculate persona scores
    nsubj_df['persona_score'] = nsubj_df['count'] * nsubj_df['agent_score']
    dobj_df['persona_score'] = dobj_df['count'] * dobj_df['theme_score']

    # Group by persona and sum the scores
    persona_nsubj_scores = nsubj_df.groupby('persona')['persona_score'].sum()
    persona_dobj_scores = dobj_df.groupby('persona')['persona_score'].sum()

    # Combine nsubj and dobj scores
    persona_scores = persona_nsubj_scores.add(persona_dobj_scores, fill_value=0).to_dict()

    # Calculate persona counts
    persona_nsubj_counts = nsubj_df.groupby('persona')['count'].sum()
    persona_dobj_counts = dobj_df.groupby('persona')['count'].sum()

    # Combine nsubj and dobj counts
    persona_counts = persona_nsubj_counts.add(persona_dobj_counts, fill_value=0).to_dict()


    # Normalize the scores by persona count
    normalized_scores = {
        persona: score / persona_counts[persona] if persona in persona_counts and persona_counts[persona] > 0 else 0
        for persona, score in persona_scores.items()
    }

    return normalized_scores
