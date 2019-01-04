'''
This scripts replaces a string in a text file if some other string exists.
The use case is two parameters with the same name that should be renamed depending on another parameter,
e.g. a == "Fixed"   thus, "value" get renamed into "value_fixed"
'''


import json
import os
import xml.etree.ElementTree as ET

#replace_this = "\"Enable_Maternal_Transmission\": 1,"
#replace_this = "\"Enable_Initial_Prevalence\": 0,"
#example: with_that = "\"class\": \"OutbreakIndividual\"," + str("\n") + "\t\t\t\t\t\t\"Incubation_Period_Override\": 0"
#whith_that = "\"Enable_Prevalence\": 1,"
#whith_that = "\"Enable_Initial_Prevalence\": 1,"
#replace_this = "\"Death_Rate_Dependence\" : \"NONDISEASE_MORTALITY_BY_AGE_AND_GENDER\","
#whith_that = replace_this + str("\n") + "\"Enable_Natural_Mortality\": test,"

replace_this = "Reporting_Period_Width"
#replace_this = "Base_Infectious_Period"

with_that = None

#use json error file from build server, e.g. 'failed_tests_2017_05_05_01_15_32_198000.json'
def getDirectoriesFromJson(json_error_report):
    '''returns a list of directories, usually relative to directory Regression'''
    with open(json_error_report, 'r') as f:
        j = json.load(f)
    dir_list = os.path.normcase(j['tests'] + "/")
    #  or  config_file_path = t['path']+ "/" + add_to ???
    return dir_list
    
    
def getDirectoriesFromXml(regression_path, error_report):
    '''returns a list of directories with failed tests, usually relative to directory Regression'''
    list = []
    tree = ET.parse(error_report)
    root = tree.getroot()
    for child in root:
        if not child.get('message') is None and  "PASSED" in child.get('message'):
            continue
        if not child.get('name') is None:
            list.append(os.path.normcase(regression_path + "/" + child.get('name') + "/"))
    return list


def getFilesFromSubDir(path, filter_fct, list):
    ''' returns files (with path) as a list to every file in a directory which maches the passed filter_fct criteria'''
    for file in [f for f in os.listdir(path) if filter_fct(f)]:
        filepath = path + "/" + file
        list.append(os.path.normcase(filepath))
    for file in [f for f in os.listdir(path) if os.path.isdir(path+"/"+f)]:
        subdir = path+"/"+ file
        print ("checking:", subdir)
        getFilesFromSubDir(subdir, filter_fct, list)
    return list


def found_fct(content, text):
    for line in content:
        if text.replace(" ", "") in line.replace(" ", ""):
            return True
    return False

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Changing config does not make sense for regression tests!!!
# config.json is generated from the defaults....json and parameter_override.json
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#use directory
WorkingDir = os.path.normcase(r"C:\Users\tfischle\GitHub\DtkTrunk_master\Regression")
#WorkingDir = os.getcwd()

errors = []

#dirs = getDirectoriesFromXml(WorkingDir,'report_2017_09_05_20_35_37_947000.xml')
file_list = []
dirs = getFilesFromSubDir(WorkingDir, lambda x: ".json" in x, file_list)    #only .json files

for t in dirs:
    #campaign_file = t['path'] + "/campaign.json"
    #campaign_file = t + "config.json"
    campaign_file = t
    print (campaign_file)

    # Replace variables in file
    try:
        with open(campaign_file, 'r') as f:
            content = [l for l in f.readlines()]  # put lines in table

            if found_fct(content, "\"Reporting_Period_Distribution\": \"LOG_NORMAL_DURATION\""):
                with_that = "Reporting_Period_Log_Normal_Width"
#            elif found_fct(content, "\"Incubation_Period_Distribution\": \"GAUSSIAN_DURATION\""):
#                with_that = "Incubation_Period_Exponential"
            else:
                continue

            found = False
            exists_already = False
            for line in content:
                if with_that in line:
                    exists_already = True
                    break   #check if already existing
            if not exists_already:
                for line in content:
                    if replace_this.replace(" ", "") in line.replace(" ", ""):
                        print ("found")
                        found = True
                        # replace string in content directly. How? replace, then to convert to string?
                        break
                if found:
                    # save content, need to figure out how, mean while use old method
                    f.close()
                    with open(campaign_file, 'r+') as f:
                        filecontent = f.read()  # filecontent is a long string
                        f.seek(0)
                        f.truncate()
                        f.write(filecontent.replace(replace_this, with_that)) # we are replacing a substring
                        f.close()

                    #rewrite json to get proper formatting
                    with open(campaign_file, 'r') as f:
                        j = json.load(f)
                    with open(campaign_file, 'w') as f:
                        json.dump(j, f, sort_keys=True, indent=4, separators=(',', ': '))

                     # write param_override.json
                    file_override = os.path.dirname(campaign_file) + "\\param_overrides.json"
                    with open(file_override, 'r+') as f:
                        filecontent = f.read()  # filecontent is a long string
                        f.seek(0)
                        if replace_this not in filecontent:
                            f.close()
                            continue
                        f.truncate()
                        f.write(filecontent.replace(replace_this, with_that)) # we are replacing a substring
                        f.close()

                    #rewrite json to get proper formatting
                    with open(file_override, 'r') as f:
                        j = json.load(f)
                    with open(file_override, 'w') as f:
                        json.dump(j, f, sort_keys=True, indent=4, separators=(',', ': '))


                else:
                     print ("NOT REPLACED IN: ", t)
    except Exception as e:
        print(e)
        errors.append(campaign_file)

print (errors)
    



# Older version, filters only for filename, newer function more general    
#def getFilesFromSubDir(path, filename, list):
#    for file in [f for f in os.listdir(path) if f == filename]:
#        filepath = path + "/" + file
#        list.append(filepath)
#    for file in [f for f in os.listdir(path) if os.path.isdir(path+"/"+f)]:
#        subdir = path+"/"+ file
#        print "checking:", subdir
#        getFilesFromSubDir(subdir, filename, list)
#    return list
        

# old: take spaces from line before. Now we are just rewriting the json file
# spaces = line[0:line.find(replace_this)]
# # with_that = replace_this + str("\n") + spaces + whith_that # this line was meant to add a parameter (replace existing param with existing + new param)
# with_that = whith_that
