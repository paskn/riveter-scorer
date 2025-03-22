import re


def get_dicts_from_txt(file_path):
    namespace = {}
    # Read and execute the .txt file
    with open(file_path, 'r') as file:
        content = file.read()
    # handle possesives with 's
    content = re.sub(r"\'s\s", r' ', content)
    # handle won't
    content = re.sub(r"won\'t.\w+", r"will_not", content)
    exec(content, namespace)
    # Access the dictionaries from the namespace
    nsubj_verb_count_dict = namespace['nsubj_verb_count_dict']
    dobj_verb_count_dict = namespace['dobj_verb_count_dict']
    return nsubj_verb_count_dict, dobj_verb_count_dict
