import re


def get_dicts_from_txt(file_path):
    # Initialize dictionaries to store cumulative results
    nsubj_verb_count_dict = {}
    dobj_verb_count_dict = {}
    
    # Read the file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Handle possessives with 's
    content = re.sub(r"\'s\s", r' ', content)
    # Handle won't
    content = re.sub(r"won\'t.\w+", r"will_not", content)
    
    # Find the dictionary definitions using regex
    nsubj_match = re.search(r"nsubj_verb_count_dict\s*=\s*\{(.*?)\}", content, re.DOTALL)
    dobj_match = re.search(r"dobj_verb_count_dict\s*=\s*\{(.*?)\}", content, re.DOTALL)
    
    if nsubj_match:
        nsubj_entries = re.findall(r"\(\s*['\"](.*?)['\"]\s*,\s*['\"](.*?)['\"]\s*\)\s*:\s*(\d+)", nsubj_match.group(1))
        for subject, verb, count in nsubj_entries:
            key = (subject, verb)
            if key in nsubj_verb_count_dict:
                nsubj_verb_count_dict[key] += int(count)
            else:
                nsubj_verb_count_dict[key] = int(count)
    
    if dobj_match:
        dobj_entries = re.findall(r"\(\s*['\"](.*?)['\"]\s*,\s*['\"](.*?)['\"]\s*\)\s*:\s*(\d+)", dobj_match.group(1))
        for object, verb, count in dobj_entries:
            key = (object, verb)
            if key in dobj_verb_count_dict:
                dobj_verb_count_dict[key] += int(count)
            else:
                dobj_verb_count_dict[key] = int(count)
    
    return nsubj_verb_count_dict, dobj_verb_count_dict
