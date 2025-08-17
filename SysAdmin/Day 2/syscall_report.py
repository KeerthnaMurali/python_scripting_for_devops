import argparse
import subprocess
parser = argparse.ArgumentParser(description="Enter the command")
parser.add_argument("--command", nargs="+", required=True, help="command to execute")
args= parser.parse_args()

#call the strace
result = subprocess.run(["strace", "-f","-c", "--"] + args.command, capture_output=True, text=True)

print("Return code:", result.returncode)  # 0 means success
print("Output:\n", result.stdout)
print("Errors:\n", result.stderr)

lines = result.stderr.splitlines()


for i, line in enumerate(lines):
    if line.startswith("%time"):
        start = i+1
        break

if start is not None:
    output = []
    for line in lines[start:]:
        if line.startswith("------") or line.strip().endswith("total"):
            break
        output.append(line)