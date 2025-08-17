import json
import os
import glob
import sys

# from Day3.analyze_errors import output


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <directory_path>", file=sys.stderr)
    sys.exit(1)

directory = sys.argv[1]

#stp1 get the directory
# directory = input('Enter the path')
#find the json files
pattern = os.path.join(directory,"*.json")
#use glob to merge
files = sorted(glob.glob(pattern))
#if no files
if not files:
    print(f"No JSON files found in {directory}", file=sys.stderr)
    sys.exit(1)

#opn json
for file in files:
    try:
        with open(file,'r') as jsonFile:
            data = json.load(jsonFile)
            if not isinstance(data,dict):
                print("not a json object")
                continue
            merged = {}
            # inside the loop, after verifying `data`:
            merged.update(data)
            print(f"Merged {jsonFile}")

            output = os.path.join(directory,"merged.json")
            with open(output, 'w') as out:
                json.dump(merged,out,indent=2)
                out.write('\n')


    except json.JSONDecodeError as e:
        print(f"{e}")








