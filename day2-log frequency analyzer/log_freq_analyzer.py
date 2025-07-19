import json
import re

def log_analyzer():

    freqIP = {}
    result = []
    ip = 0
    skipped = 0
    pattern = re.compile(r'''
   (?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]) \. #first 
   (?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]) \. # second 
   (?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]) \. #third 
   (?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]) 
    ''', re.VERBOSE)
    with open ('./access.log', 'r') as file, \
            open('./ip_summary.json','w') as jfile, \
    open('./error.log','w') as errorfile:
        for line in file:
            match = pattern.search(line)
            if match:
                ip=match.group()
                freqIP[ip] = freqIP.get(ip,0) + 1


            else:
                skipped += 1
                result.append(line)

        json.dump(freqIP,jfile, indent=4)
        errorfile.writelines(result)




print(log_analyzer())