NEW_LINE = str("\n")

import json

add_this = {"Enable_Immunity_Distribution":1,"Enable_Initial_Prevalence":1}
add_to = 'config.json'

with open('failed_tests_2017_05_05_01_15_32_198000.json', 'r') as f:
    j = json.load(f)

for t in j['science']:
    config_file = t['path']+ "/" + add_to
    print config_file

    


        

