'''
- Replaces strings in files
- replacing of string can be conditioned on simulation types
- replace line based on matching substring e.g. to delete a line
'''


import json
import os
import argparse
import utils
from multiprocessing import Pool

#Constants
All_sim_types = ["GENERIC_SIM", "VECTOR_SIM", "MALARIA_SIM", "ENVIRONMENTAL_SIM", "POLIO_SIM", "AIRBORNE_SIM", "TB_SIM", "TBHIV_SIM", "STI_SIM", "HIV_SIM", "PY_SIM", "TYPHOID_SIM", "DENGUE_SIM"]

# add_table=[
#             [{"Enable_Immunity_Distribution": 0,
#                "Enable_Initial_Prevalence": 0,
#                "Enable_Maternal_Infection_Transmission": 0,
#                "Enable_Maternal_Protection": 0,
#                "Enable_Natural_Mortality": 0,
#                "Enable_Susceptibility_Scaling": 0,
#                "Enable_Disease_Mortality":0,
#                "Enable_Maternal_Antibodies_Transmission":0}, All_sim_types],
#             [{"Enable_Skipping": 0}, ["GENERIC_SIM", "TB_SIM"]]
#         ]

add_table=[
            [{"Symptomatic_Infectious_Offset": 0}, "", utils.condition_sim_type, All_sim_types]
        ]


replace_table = [
        ["Expiration_Period_1", "Expiration_Period_Mean_1", utils.condition_sim_type, All_sim_types, utils.RenameParam, utils.comp_param],
        ["Expiration_Period_2", "Expiration_Period_Mean_2", utils.condition_sim_type, All_sim_types, utils.RenameParam, utils.comp_param],
        ["Expiration_Period_Percentage_1", "Expiration_Period_Proportion_1", utils.condition_sim_type, All_sim_types, utils.RenameParam, utils.comp_param],
        ["FIXED_DURATION", "CONSTANT_DISTRIBUTION", utils.condition_sim_type, All_sim_types, utils.RenameValue, utils.comp_value],
        ["EXPONENTIAL_DURATION", "EXPONENTIAL_DISTRIBUTION", utils.condition_sim_type, All_sim_types, utils.RenameValue, utils.comp_value],
        ["GAUSSIAN_DURATION", "GAUSSIAN_DISTRIBUTION", utils.condition_sim_type, All_sim_types, utils.RenameValue, utils.comp_value],
        ["LOG_NORMAL_DURATION", "LOG_NORMAL_DISTRIBUTION", utils.condition_sim_type, All_sim_types, utils.RenameValue, utils.comp_value],
        ["BIMODAL_DURATION", "DUAL_CONSTANT_DISTRIBUTION", utils.condition_sim_type, All_sim_types, utils.RenameValue, utils.comp_value],
        ["UNIFORM_DURATION", "UNIFORM_DISTRIBUTION", utils.condition_sim_type, All_sim_types, utils.RenameValue, utils.comp_value],
        ["POISSON_DURATION", "POISSON_DISTRIBUTION", utils.condition_sim_type, All_sim_types, utils.RenameValue, utils.comp_value],
        ["DUAL_TIMESCALE_DURATION", "DUAL_EXPONENTIAL_DISTRIBUTION", utils.condition_sim_type, All_sim_types, utils.RenameValue, utils.comp_value],
        ["WEIBULL_DURATION", "WEIBULL_DISTRIBUTION", utils.condition_sim_type, All_sim_types, utils.RenameValue, utils.comp_value],
        ["_Separation", "_Peak_2_Value", utils.condition_sim_type, All_sim_types, utils.ReplaceParamEndswith, utils.comp_param_endswith],
#       ["_1", "_Mean_1", All_sim_types, utils.Rename, utils.ReplaceParamEndswith, utils.comp_param_endswith],
#       ["_2", "_Mean_2", All_sim_types, utils.Rename, utils.ReplaceParamEndswith, utils.comp_param_endswith],
        ["_Peak1", "_Proportion_0", utils.condition_sim_type, All_sim_types, utils.ReplaceParamEndswith, utils.comp_param_endswith],
        ["_Fixed", "_Constant", utils.condition_sim_type, All_sim_types, utils.ReplaceParamEndswith, utils.comp_param_endswith],
        ["DistributionFixed", "DistributionConstant", utils.condition_sim_type, All_sim_types, utils.RenameValue, utils.comp_value],
        ["Base_Infectious_Period", "Infectious_Period_Constant", utils.condition_param_exists, {"Infectious_Period_Distribution": "CONSTANT_DISTRIBUTION"}, utils.RenameParam, utils.comp_param],
        ["Base_Incubation_Period", "Incubation_Period_Constant", utils.condition_param_exists, {"Incubation_Period_Distribution": "CONSTANT_DISTRIBUTION"}, utils.RenameParam, utils.comp_param],
        ["Base_Infectious_Period", "Infectious_Period_Exponential", utils.condition_param_exists, {"Infectious_Period_Distribution": "EXPONENTIAL_DISTRIBUTION"}, utils.RenameParam, utils.comp_param],
        ["Base_Incubation_Period", "Incubation_Period_Exponential", utils.condition_param_exists, {"Incubation_Period_Distribution": "EXPONENTIAL_DISTRIBUTION"}, utils.RenameParam, utils.comp_param],
        ["TB_Active_Period_Std_Dev", "TB_Active_Period_Gaussian_Std_Dev", utils.condition_exists, {"TB_Active_Period_Distribution": "GAUSSIAN_DISTRIBUTION"}, utils.RenameParam, utils.comp_param],
        ["TB_Active_Period_Mean", "TB_Active_Period_Gaussian_Mean", utils.condition_exists,{"TB_Active_Period_Distribution": "GAUSSIAN_DISTRIBUTION"}, utils.RenameParam, utils.comp_param],
        ["Infectious_Period_Std_Dev", "Infectious_Period_Gaussian_Std_Dev", utils.condition_exists, {"Infectious_Period_Distribution": "GAUSSIAN_DISTRIBUTION"}, utils.RenameParam, utils.comp_param],
        ["Infectious_Period_Mean", "Infectious_Period_Gaussian_Mean", utils.condition_exists, {"Infectious_Period_Distribution": "GAUSSIAN_DISTRIBUTION"}, utils.RenameParam, utils.comp_param],
        ["_Log_Normal_Mean", "_Log_Normal_Mu", utils.condition_sim_type, All_sim_types, utils.ReplaceParamEndswith, utils.comp_param_endswith],
        ["_Log_Normal_Width", "_Log_Normal_Sigma", utils.condition_sim_type, All_sim_types, utils.ReplaceParamEndswith, utils.comp_param_endswith],
        ["Duration_Before_Leaving_Distribution_Type", "Duration_Before_Leaving_Distribution", utils.condition_sim_type, All_sim_types, utils.ReplaceParamEndswith, utils.comp_param_endswith],
        ["Duration_At_Node_Distribution_Type", "Duration_At_Node_Distribution", utils.condition_sim_type, All_sim_types, utils.ReplaceParamEndswith, utils.comp_param_endswith],
        ["Risk_Distribution_Type", "Risk_Distribution", utils.condition_sim_type, All_sim_types, utils.ReplaceParamEndswith, utils.comp_param_endswith],
        ["Initial_Amount_Distribution_Type", "Initial_Amount_Distribution", utils.condition_sim_type, All_sim_types, utils.ReplaceParamEndswith, utils.comp_param_endswith],
#        ["x_Temporary_Larval_Habitat", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
#        ["x_Temporary_Larval_Habitat", "x_Larval_Habitats", utils.condition_sim_type, All_sim_types, utils.RenameParam, utils.comp_param],
    # remove unused parameterss
["Polio_Host_Factor", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Immunity_Initialization_Distribution_Type", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Enable_Immunity_Distribution", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Enable_Vector_Migration_Wind", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["HIV_CoInfection_Probability", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Environmental_Incubation_Period", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Heterogeneous_Infectiousness_Weibull_Scale", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],


["Enable_Demographics_Other", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Susceptibility_Scale_Type", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Enable_Default_Shedding_Function", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Enable_Time_Dep_Birth", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Heterogeneous_Infectiousness_Weibull_Heterogeneity", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Viral_Replication_Latent_Reservoir_Exit_Rate", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["CoInfected_Mortality_Rate", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],

["Viral_Replication_Infected_Cell_Death_Rate", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Typhoid_Carrier_Removal_Year", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Enable_Time_Dep_Mortality", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Viral_Replication_R0", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Infectious_Period_Std_Dev", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Typhoid_Exposure_1990", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Visiting_Pool_Selection_Mode", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],

["Random_Type", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Enable_Demographics_Gender", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Typhoid_Carrier_Probability_Female", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Enable_Absolute_Time", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Typhoid_Environmental_Peak_Multiplier", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["STI_Coinfection_Probability", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Individual_PK_Heterogeneity", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],

["Infectious_Period_Mean", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["HIV_coinfection_probability", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
# Egg_Survival_Rate used in C:\Users\tfischle\Github\DtkTrunk\Regression\Dengue\SFTs\VectorEggOvercrowding_NaturalMortality\dtk_post_process.py
#["Egg_Survival_Rate", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Enable_Vector_Migration_Human", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Typhoid_Exposure_1991", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Environmental_Ramp_Duration", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Enable_Delayed_Hatching_When_Habitat_Dries_Up", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],

["Enable_Timestep_Channel_In_Report", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Pool_Transmission_Mode", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Viral_Replication_Residual_VL", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["Typhoid_Carrier_Probability_Male", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],
["TB_Smear_Negative_Infectious_Multiplier", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param],




# Those parameters have to renmaded as well
# •	Infectious_Period_Std_Dev     LOG_NORMAL
# •	Infectious_Period_Mean        LOG_NORMAL
# •	Constant
# •	Initial_Amount
        ["x_Population_Immunity", "", utils.condition_sim_type, All_sim_types, utils.DeleteLine, utils.comp_param]
]

DefaultSimType = "HIV_SIM"

def getCommandLineArgs():
    parser = argparse.ArgumentParser(description='renames distribution parameters')
    parser.add_argument("-r", action='store_true', default=False, help="recursive search in subdirectories")
    parser.add_argument("-addNewParameters", action='store_true', default=False, help="add new 2.14 parameters to config, otherwise only replace and delete e.g. for demographics files")
    parser.add_argument("-sortJson", action='store_true', default=False, help="sort the configuration parameters in alphabetic order")
    parser.add_argument("directory", nargs='?', default=".", help="directory where the configuration file(s) to be converted are located (default = . )")
    parser.add_argument("file_name",nargs='?', default="config.json", help="filename for file(s) that should be converted. With -r all files that end with file_name (e.g. config.json converts test_config.json) are found as well. (default = config.json)")
    parser.add_argument("-replace_table", nargs='?', default=[], help="pass your own replace table to the script e.g. [[\"TB_Drug_Cure_Rate\",\"\",\"All_sim_types\",1]]. Quotes have to preceded by a slash \\.")
    args = parser.parse_args()
    return args

def replace(fct_params):
    config_file = fct_params[0]
    addNewParameters = fct_params[1]
    sortJson = fct_params[2]
    replaced = False  # File changed?
    print("Opening: ", config_file)
    # try to determine sim type and add parameters
    with open(config_file, 'r+') as f:
        try:
            j = json.load(f)
        except Exception as e:
            print("Error could not load :", config_file, "\n",  e)
            #continue
            return #multiprocessing
        # if "parameters" in j.keys():
        #     if "Simulation_Type" in j["parameters"].keys():
        #         sim_type = j["parameters"]["Simulation_Type"]    # works only in config.json
        #     else:
        #         sim_type = guessSimTypeFromFileName(config_file) if guessSimTypeFromFileName(config_file) is not None else DefaultSimType
        # else:
        #sim_type = guessSimTypeFromFileName(config_file) if guessSimTypeFromFileName(config_file) is not None else DefaultSimType

        sim_type = DefaultSimType

        if addNewParameters:
            for row in add_table:
                if row[utils.Idx_condition_fct](sim_type, None, row):
                    for key, val in row[0].items():
                        if 'parameters' in j:
                            if j['parameters'].get(key, None) is None:      # add under "parameters"
                                j['parameters'][key]=val
                                replaced = True
                        else:
                            if j.get(key, None) is None:
                                j[key]=val
                                replaced = True

        replaced = utils.replace_in_dict(j, replace_table, sim_type) or replaced

        if replaced:
            f.seek(0)
            f.truncate()
            #new_file = '\n'.join(str(line) for line in content) #create string
            json.dump(j, f, sort_keys=sortJson, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    #use directory
    #WorkingDir = os.path.normcase(r"C:\\Users\\tfischle\\Github\\DtkTrunk_master_213\\Regression\\Multicore_Nosibe\\42_Vector_SimpleIndividualRepellent")
    #name_config_file = "config.json"    # sub strings like ".json", "overrides.json" works as well
    commandline_args = getCommandLineArgs()
    WorkingDir = os.path.normpath(commandline_args.directory)
    name_config_file = commandline_args.file_name

    if commandline_args.r:
        file_list = []
        dirs = utils.getFilesFromSubDir(WorkingDir, name_config_file, file_list)
    else:
        dirs = [WorkingDir + "\\" + name_config_file]

    if commandline_args.replace_table:
        replace_table = json.loads(commandline_args.replace_table)
        for idx, row in enumerate(replace_table):
            if row[utils.Idx_condition_fct] == "All_sim_types":
                replace_table[idx][utils.Idx_condition_fct] = All_sim_types

    print("converting: ", [os.path.normpath(f) for f in dirs])

    fct_params = [[dir, commandline_args.addNewParameters, commandline_args.sortJson] for dir in dirs]

#    for param in fct_params:
#        replace(param)

    with Pool(processes=20) as pool:
        pool.map(replace, fct_params)


    # with open(config_file, 'w') as f:
    #     json.dump(j, f, sort_keys=True, indent=4, separators=(',', ': '))

    # with open(config_file, 'r+') as f:
    #     j = json.load(f)