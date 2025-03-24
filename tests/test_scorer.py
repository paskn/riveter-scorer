import os
from riveter_scorer.scorer import load_sap_lexicon_as_dict
from riveter_scorer.scorer import calculate_power_score
from riveter_scorer.helpers import get_dicts_from_txt 
from riveter_scorer.helpers import are_dicts_identical 


def test_get_dicts_from_txt():
    # file_path = "tests/data/verbs.ya.Caundy.Matched.txt"
    file_path = "tests/data/example_stories.txt"
    nsubj_verb_count_dict, dobj_verb_count_dict = get_dicts_from_txt(file_path)
    print(dobj_verb_count_dict)
    assert len(nsubj_verb_count_dict) == 13
    # should be 9 not 10 because a ('doctor', 'thank'): 1 is duplicated
    assert len(dobj_verb_count_dict) == 9

    
def test_load_sap_lexicon_as_dict():
    sap = os.path.join(os.getcwd(), 'data', 'sap-lexicon', 'agency_power.csv')
    agency = load_sap_lexicon_as_dict(sap, dimension='agency')
    assert len(agency) == 2148
    power = load_sap_lexicon_as_dict(sap, dimension='power')
    assert len(power) == 2148

    
def test_calculate_power_score():
    file_path = "tests/data/example_stories.txt"
    nsubj_verb_count_dict, dobj_verb_count_dict = get_dicts_from_txt(file_path)
    sap = os.path.join(os.getcwd(), 'data', 'sap-lexicon', 'agency_power.csv')
    agency = load_sap_lexicon_as_dict(sap, dimension='agency')
    agency_scores = calculate_power_score(nsubj_verb_count_dict, dobj_verb_count_dict, agency)
    print(agency_scores)

    riveter_ref = {
        'i': 0.1,
        'she': 0.3333333333333333,
        'car': 1.0,
        'tree': 0.0,
        'doctor': 0.16666666666666666,
        'susan': 0.0,
        'mary': 0.3333333333333333,
        # riveter will not consider these at all
        'it': 0.0,
        'jack': 1.0,
        'vase': 0.0
    }
    
    assert are_dicts_identical(agency_scores, riveter_ref) == True
