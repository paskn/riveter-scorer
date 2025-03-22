import os
from riveter_scorer.scorer import load_sap_lexicon_as_dict
from riveter_scorer.helpers import get_dicts_from_txt 


def test_get_dicts_from_txt():
    file_path = "tests/data/verbs.ya.Caundy.Matched.txt"
    nsubj_verb_count_dict, dobj_verb_count_dict = get_dicts_from_txt(file_path)
    assert len(nsubj_verb_count_dict) == 3418
    assert len(dobj_verb_count_dict) == 2016

    
def test_load_sap_lexicon_as_dict():
    sap = os.path.join(os.getcwd(), 'data', 'sap-lexicon', 'agency_power.csv')
    agency = load_sap_lexicon_as_dict(sap, dimension='agency')
    assert len(agency) == 2148
    power = load_sap_lexicon_as_dict(sap, dimension='power')
    assert len(power) == 2148
    

# power_scores = calculate_power_score(nsubj_verb_count_dict, dobj_verb_count_dict, verb_score_dict)
# print(power_scores)
# out = file_path+"_agency-score.json"
# with open(out, "w") as dump:
#     json.dump(power_scores, dump, indent=4)
#     print(f"Scores saved into {out}")
    
