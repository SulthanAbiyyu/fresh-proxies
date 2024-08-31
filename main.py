import os
from get_proxies import get_proxies
from check_proxies import check_proxy

def main():
    valid_proxies = []

    if os.path.exists("valid_proxies.txt"):
        print("Checking if existing proxies are still valid...")
        still_valid = check_proxy("valid_proxies.txt")
        print(f"Found {len(still_valid)} valid proxies from the existing list.")
        valid_proxies += still_valid

    print("Fetching new proxies...")
    new_proxies = get_proxies()
    print(f"Fetched {len(new_proxies)} new proxies.")

    with open("proxies.txt", "w") as f:
        for i in new_proxies:
            f.write(i + "\n")
    print("New proxies have been written to 'proxies.txt'.")

    print("Checking the validity of new proxies...")
    new_valid_proxies = check_proxy("proxies.txt")
    print(f"Found {len(new_valid_proxies)} valid proxies from the new list.")
    valid_proxies += new_valid_proxies

    with open("valid_proxies.txt", "w") as f:
        for i in valid_proxies:
            f.write(i + "\n")
    print(f"Total valid proxies written to 'valid_proxies.txt': {len(valid_proxies)}")

if __name__ == "__main__":
    main()