import os
print()
import subprocess
def pr():
    print(os.listdir())
    result = subprocess.run(
        ["echo", "Hello from subprocess"],
        capture_output=True,
        text=True
    )
    print("Output:", result.stdout.strip())

if __name__=="__main__":
    pr()