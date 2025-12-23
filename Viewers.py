import requests
import threading
import time

URL = input('Enter the URL: ')
REQUESTS_PER_SECOND = int(input('Enter the amount of Threads: '))

total_requests = 0

def make_requests():
    global total_requests
    while True:
        requests.get(URL)
        total_requests += 1 
        time.sleep(1 / REQUESTS_PER_SECOND)

def print_progress():
    print(" ")
    while True:
        print(f"Total successful requests made: {total_requests}")
        time.sleep(1)

def main():
    threads = []
    for _ in range(REQUESTS_PER_SECOND):
        thread = threading.Thread(target=make_requests)
        threads.append(thread)
        thread.start()

    progress_thread = threading.Thread(target=print_progress)
    progress_thread.start()

    for thread in threads:
        thread.join()

    progress_thread.join()

if __name__ == "__main__":
    main()
