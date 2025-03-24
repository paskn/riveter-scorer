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


def are_dicts_identical(dict1, dict2):
    """
    Check if two dictionaries have identical keys and values.
    If there are differences, print what doesn't match.
    
    Args:
        dict1: First dictionary to compare
        dict2: Second dictionary to compare
        
    Returns:
        bool: True if dictionaries have identical keys and values, False otherwise
    """
    # Check if they have the same keys
    if dict1.keys() != dict2.keys():
        # Find keys in dict1 but not in dict2
        keys_only_in_dict1 = set(dict1.keys()) - set(dict2.keys())
        if keys_only_in_dict1:
            print(f"Keys present in first dict but missing in second: {keys_only_in_dict1}")
        
        # Find keys in dict2 but not in dict1
        keys_only_in_dict2 = set(dict2.keys()) - set(dict1.keys())
        if keys_only_in_dict2:
            print(f"Keys present in second dict but missing in first: {keys_only_in_dict2}")
        
        return False
    
    # Check if each key has the same value in both dictionaries
    all_match = True
    for key in dict1:
        if dict1[key] != dict2[key]:
            print(f"Value mismatch for key: {key}")
            print(f"  - First dict[{key}]: {dict1[key]}")
            print(f"  - Second dict[{key}]: {dict2[key]}")
            all_match = False
    
    return all_match
