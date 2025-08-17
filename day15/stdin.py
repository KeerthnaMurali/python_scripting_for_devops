#!/usr/bin/env python3
import sys

def main():
    # Read every line from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        # Example processing: uppercase each line
        print(line.upper())

if __name__ == "__main__":
    main()