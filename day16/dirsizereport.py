import os
from collections import defaultdict

import psutil
from psutil import NoSuchProcess

# print(psutil.__all__)
def function():
    dir = input("Enter the path")
    try:
        subdir = os.listdir(dir)
    except FileNotFoundError as e:
        print(f"File not found{e}")
    d = defaultdict(lambda x:[0,"",0])
    for process in psutil.process_iter(attrs=['pid','name','memory_info']):
        try:
            p = process.info
            id = p['pid']
            name = p['name']
            mem = p['mem_info'].rss / 1024 * 1024
            print(f"{id:>6} {name:<25} {mem:.6.2f} ")




                #
                # print(f"{pid:>6}  {mem:>20}")
                #
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass



if __name__=="__main__":
    function()