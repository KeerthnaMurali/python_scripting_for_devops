import re
import subprocess
import argparse
import logging
from cgitb import handler
def parse_size(s: str) -> int:
    s = s.strip().upper()
    units = {"B":1, "KB":1024, "MB":1024**2, "GB":1024**3}
    for u in ("GB","MB","KB","B"):
        if s.endswith(u):
            return int(float(s[:-len(u)].strip()) * units[u])
    return int(s)

from logging.handlers import RotatingFileHandler
parser = argparse.ArgumentParser( description="Enter the regex pattern")
parser.add_argument("--regex", required=True,help="command to execute")
parser.add_argument("--input",required=True,help="file to input" )
parser.add_argument("--out",default="filtered.log", help="Output file (rotates)" )
parser.add_argument("--maxsize", default="1KB", help="Max size before rotate (e.g., 10MB)")
parser.add_argument("--backups", type=int, default=5, help="Number of rotated backups")
args = parser.parse_args()

#fined the error
pattern = re.compile(args.regex)




logger = logging.getLogger("my_app_logger")
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler(filename=args.out,
    mode="a",
    maxBytes=parse_size(args.maxsize),
    backupCount=args.backups,
    encoding="utf-8",)
logger.addHandler(handler)

popen = subprocess.Popen(["tail", "-n","1000", args.input], stdout=subprocess.PIPE, text=True)

try:
    for line in popen.stdout:
        if pattern.findall(line):
            logger.error(line.rstrip("\n"))

except KeyboardInterrupt:
    pass

finally:
        try:
            popen.terminate()
        except Exception:
            pass



