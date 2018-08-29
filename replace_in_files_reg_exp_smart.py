import json

replace_this = "\"class\": \"OutbreakIndividual\""
with_that = "\"class\": \"OutbreakIndividual\"," + str("\n") + "\t\t\t\t\t\t\"Incubation_Period_Override\": 0"

with open('failed_tests_2017_05_05_01_15_32_198000.json', 'r') as f:
    j = json.load(f)

for t in j['tests']:
    campaign_file = t['path']+ "/campaign.json"
    print campaign_file

    # Replace variables in file
    with open(campaign_file, 'r') as f:
        content = [l for l in f.readlines()]    # put lines in table
        for line in content:
            if replace_this in line:
                print "found"
                spaces = line[0:line.find(replace_this)]
                with_that = "\"class\": \"OutbreakIndividual\"," + str("\n") + spaces + "\"Incubation_Period_Override\": 0"

                # replace string in line, how?
                break
        # save content, need to figure out how, mean while use old method
    f.close()
    f = open(campaign_file, 'r+')
    filecontent = f.read()
    f.seek(0)
    f.truncate()
    f.write(filecontent.replace(replace_this, with_that))
    f.close()

    


        

