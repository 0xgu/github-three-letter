import sys, requests
from tqdm import tqdm
from multiprocessing import Process, freeze_support
import time 

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
        f.close()

if __name__ == "__main__":
    freeze_support()

    try:
        lc = 0
        lines = open("letters.txt").read().splitlines()
        lc = len(lines)
        processes = []
        for i in tqdm(range(0, lc)):
            p = Process(target=request, args=(lines[i],))
            processes.append(p)
            p.start()
            time.sleep(0.1)
        while True:
            for p in processes:
                if not p.is_alive():
                    processes.remove(p)
            if len(processes) == 0:
                break
            time.sleep(0.1)
            pass
    except KeyboardInterrupt:
        sys.exit()
        f.close()
