import os

# Functions
def getFilesFromSubDir(path, file_name, file_list=[]):
    ''' returns files (with path) as a list to every file in a directory that maches the passed filter_fct criteria'''
    for file in [f for f in os.listdir(path) if file_name in f]:
        filepath = path + "/" + file
        file_list.append(os.path.normcase(filepath))
    for file in [f for f in os.listdir(path) if os.path.isdir(path+"/"+f)]:
        subdir = path+"/"+ file
        print ("checking:", subdir)
        getFilesFromSubDir(subdir, file_name, file_list)
    return file_list

def guessSimTypeFromFileName(file_path):
    file_name = os.path.basename(file_path).lower()
    if "tb" in file_name:
        return "TB_SIM"
    if "malaria" in file_name:
        return "MALARIA_SIM"
    if "polio" in file_name:
        return "POLIO_SIM"
    if "generic" in file_name:
        return "GENERIC_SIM"
    if "hiv" in file_name:
        return "HIV_SIM"
    if "sti" in file_name:
        return "STI_SIM"
    if "typhoid" in file_name:
        return "TYPHOID_SIM"
    if "vector" in file_name:
        return "VECTOR_SIM"
    if "dengue" in file_name:
        return "DENGUE_SIM"
    return None



#Constants
Idx_replace_this = 0
Idx_replace_whith_that = 1
Idx_condition_fct = 2
Idx_condition = 3
Idx_replace_whole_line_at_submatch = 4
Idx_compare_fct = 5


DeleteLine = 1
RenameParam = 2  # depricated
RenameValue = 3
RenameParam = 4
ReplaceParamEndswith = 5

def condition_sim_type(sim_type, dict, entry):
    return sim_type in entry[Idx_condition]

def condition_param_exists(sim_type, dict, entry):
    found = False
    for key, value in entry[Idx_condition].items():
        found = find_in_dict(dict, key, value) or found
    return found

def condition_exists(sim_type, dict, entry):
    found = False
    for key, value in entry[Idx_condition].items():
        found = find_in_dict(dict, key, value) or found
    return found


def comp_param_endswith(key, value, entry):
    return key.endswith(entry[Idx_replace_this])

def comp_value(key, value, entry):
    return entry[Idx_replace_this] == value

def comp_param(key, value, entry):
    return entry[Idx_replace_this] == key

def replace_in_dict(dic, replace_table, sim_type):
    replaced = False
    if isinstance(dic, list):
        for d in dic:
            replaced = replace_in_dict(d, replace_table, sim_type) or replaced
    elif isinstance(dic, dict):
        for key, value in dic.items():
            #print("key: ", key, "    value: ", value)
            for entry in replace_table:
                if entry[Idx_condition_fct](sim_type, dic, entry): # call condition function to see if string needs to be replaced
                    if entry[Idx_compare_fct](key, value, entry):   #call compare function defined in replace table
                        if entry[Idx_replace_whole_line_at_submatch] == DeleteLine:
                            del dic[key]
                        elif entry[Idx_replace_whole_line_at_submatch] == RenameValue:
                            dic[key] = entry[Idx_replace_whith_that]    # old entry with new value i.e. rename
                        elif entry[Idx_replace_whole_line_at_submatch] == RenameParam:
                            dic[entry[Idx_replace_whith_that]] = dic[key]    #renamed parameter with old value i.e. rename
                            del dic[key]
                        elif entry[Idx_replace_whole_line_at_submatch] == ReplaceParamEndswith:
                            new_param = key.replace(entry[Idx_replace_this], entry[Idx_replace_whith_that])
                            dic[new_param] = dic[key]    #new entry with old value i.e. rename
                            del dic[key]
                        replaced = True
            if dic.get(key, None) is not None:
                replaced = replace_in_dict(dic[key], replace_table, sim_type) or replaced
    return replaced


def find_in_dict(dic, text, value=None):
    found = False
    if isinstance(dic, list):
        for d in dic:
            found = find_in_dict(d, text, value) or found
    elif isinstance(dic, dict):
        for key in list(dic.keys()):
            # print(key)
            if text == key and value is None:
                found = True
            elif text == key and dic[text] == value:
                found = True
            if dic.get(key, None) is not None:
                found = find_in_dict(dic[key], text, value) or found
    return found

#def replace_in_dict(dic, replace_table, sim_type):
#    replaced = False
#    if isinstance(dic, list):
#        for d in dic:
#             replaced = replace_in_dict(d, replace_table, sim_type) or replaced
#     elif isinstance(dic, dict):
#         for key in list(dic.keys()):
#             #print(key)
#             for entry in replace_table:
#                 if sim_type in entry[Idx_simtypes]: #if sim_type is none we are parsing not a config.json file
#                     if entry[Idx_replace_this] == key:
#                         if entry[Idx_replace_whole_line_at_submatch] == DeleteLine:
#                             del dic[key]
#                         elif entry[Idx_replace_whole_line_at_submatch] == RenameParam:
#                             dic[entry[Idx_replace_whith_that]] = dic[key]    #new entry with old value i.e. rename
#                             del dic[key]
#                         replaced = True
#             if dic.get(key, None) is not None:
#                 replaced = replace_in_dict(dic[key], replace_table, sim_type) or replaced
#     return replaced
#
#
# def replace_in_dict2(dic, replace_table, sim_type):
#     replaced = False
#     if isinstance(dic, list):
#         for d in dic:
#             replaced = replace_in_dict2(d, replace_table, sim_type) or replaced
#     elif isinstance(dic, dict):
#         for key in list(dic.keys()):
#             #print(key)
#             for entry in replace_table:
#                 if sim_type in entry[Idx_simtypes]: #if sim_type is none we are parsing not a config.json file
#                     if key.endswith(entry[Idx_replace_this]):
#                         if entry[Idx_replace_whole_line_at_submatch] == DeleteLine:
#                             del dic[key]
#                         elif entry[Idx_replace_whole_line_at_submatch] == RenameParamEndswith:
#                             new_param = key.replace(entry[Idx_replace_this], entry[Idx_replace_whith_that])
#                             dic[new_param] = dic[key]    #new entry with old value i.e. rename
#                             del dic[key]
#                         replaced = True
#             if dic.get(key, None) is not None:
#                 replaced = replace_in_dict2(dic[key], replace_table, sim_type) or replaced
#     return replaced
