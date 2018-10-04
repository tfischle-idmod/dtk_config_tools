'''
- Tries to load a file to check if it valid json
'''
import json
import os
import argparse
import sys

Path_to_Notepad = "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"

# Functions
def getFilesFromSubDir(path, file_name, file_list):
    ''' returns files (with path) as a list to every file in a directory that maches the passed filter_fct criteria'''
    #for file in [f for f in os.listdir(path) if name_config_file in f]:
    for file in [f for f in os.listdir(path) if f.endswith(name_config_file)]:
        filepath = path + "/" + file
        file_list.append(os.path.normcase(filepath))
    for file in [f for f in os.listdir(path) if os.path.isdir(path+"/"+f)]:
        subdir = path+"/"+ file
        print ("adding:", subdir)
        getFilesFromSubDir(subdir, file_name, file_list)
    return file_list

def getCommandLineArgs():
    parser = argparse.ArgumentParser(description='renames distribution parameters')
    parser.add_argument("-r", action='store_true', default=False, help="recursive search in subdirectories")
    parser.add_argument("directory", nargs='?', default=".", help="directory where the configuration file(s) to be converted are located (default = . )")
    parser.add_argument("file_name",nargs='?', default="config.json", help="filename for file(s) that should be converted. With -r all files that end with file_name (e.g. config.json converts test_config.json) are found as well. (default = config.json)")
    args = parser.parse_args()
    return args


#use directory
#WorkingDir = os.path.normcase(r"C:\\Users\\tfischle\\Github\\DtkTrunk_master_213\\Regression\\Multicore_Nosibe\\42_Vector_SimpleIndividualRepellent")
#name_config_file = "config.json"    # sub strings like ".json", "overrides.json" works as well
commandline_args =  getCommandLineArgs()
WorkingDir = os.path.normpath(commandline_args.directory)
name_config_file = commandline_args.file_name
error_files = {}

if commandline_args.r:
    file_list = []
    dirs = getFilesFromSubDir(WorkingDir, name_config_file, file_list)
else:
    dirs = [WorkingDir + "\\" + name_config_file]

print("converting: ", [os.path.normpath(f) for f in dirs])

for config_file in dirs:
    # try to determine sim type and add parameters
    with open(config_file, 'r+') as f:
        try:
            j = json.load(f)
        except Exception as e:
            print("Error could not load :", config_file, "\n",  e)
            if not "config.json" in config_file:
                error_files[config_file] = e               
            continue
print ("--------------------- Errors ------------------")
import subprocess
for error_file in error_files:
    print(error_file, "\n", error_files[error_file], "\n")
    subprocess.call([Path_to_Notepad, error_file])