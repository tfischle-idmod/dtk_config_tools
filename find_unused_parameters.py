import utils
import argparse
import os
import json


def getCommandLineArgs():
    parser = argparse.ArgumentParser(description='compare config file (e.g. config.json) to a reference of all valid parameters (e.g. schema.json)')
    parser.add_argument("-r", action='store_true', default=False, help="recursive search in subdirectories")
    parser.add_argument("directory", nargs='?', default=".", help="directory where the configuration file(s) to be converted are located (default = . )")
    parser.add_argument("file_name",nargs='?', default="config.json", help="filename for file(s) that should be converted. With -r all files that end with file_name (e.g. config.json converts test_config.json) are found as well. (default = config.json)")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    commandline_args = getCommandLineArgs()
    WorkingDir = os.path.normpath(commandline_args.directory)
    name_config_file = commandline_args.file_name
    name_config_file = ["config.json", "param_overrides.json"]

    if commandline_args.r:
        file_list = []
        dirs = utils.getFilesFromSubDir(WorkingDir, name_config_file, file_list)
    else:
        dirs = [WorkingDir + "\\" + name_config_file]

    schema_file = os.path.normcase(r"C:\\Users\\tfischle\\Desktop\\schema.json")
    with open(schema_file, 'r+') as f:
        try:
            schema = json.load(f)
        except Exception as e:
            print("Error could not load :", schema_file, "\n", e)
            exit(-1)

    all_parameters = set()
    parameters_not_in_schema = set()

    for dir in dirs:
        config_file = dir
        with open(config_file, 'r+') as f:
            try:
                j = json.load(f)
            except Exception as e:
                print("Error could not load :", config_file, "\n", e)
                continue

            utils.get_all_keys(j, all_parameters)
            for param in all_parameters:
                if not utils.find_in_dict(schema, param):
                    #print ("Could not find in schema: ", param)
                    if "." not in param:
                        parameters_not_in_schema.add(param)

    print ("Parameters used in configuration files: ", all_parameters)
    print ("Parameters not in schema: ", parameters_not_in_schema)