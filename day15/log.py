import psutil
# Inspect the psutil module itself
#
# import psutil
# print(psutil.__all__)

def list_all_running_process():

    for process in psutil.process_iter(['pid','name','memory_info']):
        try:
            pid = process.info['pid']
            name = process.info['name']
            memory = process.memory_info().rss /  (1024 * 1024)

            print(f"{pid:>6}  {name:>20}  {memory:6.2f} MB")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

#
if __name__ == "__main__":
    list_all_running_process()





