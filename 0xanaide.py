import sys, requests
from tqdm import tqdm
from multiprocessing import Process, freeze_support
import time 
import psutil

f = open("result.txt", "a")

def request(user):
    try:
        user = user.strip()
        status = requests.get(f"https://github.com/{user}").status_code
        result = {"user": user, "data": status}
        if status == 404:
            f.write(user + "\n")
        return result
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    freeze_support()

    try:
        lc = 0
        lines = open("letters.txt").read().splitlines()
        lc = len(lines)
        processes = []
        for i in tqdm(range(0, lc)):
            cpu_usage = psutil.cpu_percent()
            if cpu_usage > 80:
                while True:
                    cpu_usage = psutil.cpu_percent()
                    if cpu_usage < 80:
                        break
                    time.sleep(0.2)
            p = Process(target=request, args=(lines[i],))
            processes.append(p)
            p.start()
            time.sleep(0.01)
            #time.sleep(0.1)
        while True:
            for p in processes:
                if not p.is_alive():
                    processes.remove(p)
            if len(processes) == 0:
                break
            time.sleep(0.1)
            pass
        f.close()
    except KeyboardInterrupt:
        sys.exit()
