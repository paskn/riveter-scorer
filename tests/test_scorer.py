# Example data (replace with your actual data)
file_path = "books/from_gemini/verbs.ya.Caundy.Matched.txt"
nsubj_verb_count_dict, dobj_verb_count_dict = get_dicts_from_txt(file_path)

lexicon_path = os.path.join(os.getcwd(), 'data', 'sap-lexicon', 'agency_power-original.csv')
verb_score_dict = load_sap_lexicon_as_dict(lexicon_path, dimension='agency')

power_scores = calculate_power_score(nsubj_verb_count_dict, dobj_verb_count_dict, verb_score_dict)
print(power_scores)
out = file_path+"_agency-score.json"
with open(out, "w") as dump:
    json.dump(power_scores, dump, indent=4)
    print(f"Scores saved into {out}")
    
