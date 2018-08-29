import json

replace_this = "\"class\": \"OutbreakIndividual\""
with_that = "\"class\": \"OutbreakIndividual\"," + str("\n") + "\t\t\t\t\t\t\"Incubation_Period_Override\": 0"

with open('failed_tests_2017_05_05_01_15_32_198000.json', 'r') as f:
    j = json.load(f)

for t in j['tests']:
    campaign_file = t['path']+ "/campaign.json"

    print replace_this
    print with_that

    # Replace variables in file
    with open(campaign_file, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.truncate()
        f.write(content.replace(replace_this, with_that))
        f.close()

    


        

