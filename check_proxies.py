import threading
import requests
import queue
from tqdm import tqdm  

def check_proxy(path):
    q = queue.Queue()
    valid_proxies = []

    # Reading proxies from file and putting them in the queue
    with open(path, "r") as f:
        for i in f.readlines():
            q.put(i.strip())

    total_proxies = q.qsize()

    def worker(progress_bar, q, valid_proxies):
        """Worker function to check proxy validity."""
        while not q.empty():
            proxy = q.get()
            try:
                response = requests.get("https://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
                if response.status_code == 200:
                    valid_proxies.append(proxy)
            except:
                pass
            finally:
                progress_bar.update(1)
                progress_bar.set_postfix(valid_proxies=len(valid_proxies))

    # Creating a progress bar
    with tqdm(total=total_proxies, desc="Checking proxies") as progress_bar:
        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(progress_bar, q, valid_proxies))
            t.start()
            threads.append(t)

        # Wait for all threads to complete
        for t in threads:
            t.join()

    return valid_proxies
