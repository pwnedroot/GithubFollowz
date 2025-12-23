import requests
import sys
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

GITHUB_API = "https://api.github.com"
USERNAME = "USERNAME_HERE"
TOKEN = "GIT_TOKEN_HERE"

session = requests.Session()

session.headers.update({
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": f"{USERNAME}-follow-back-script"
})

retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "PUT"]
)

adapter = HTTPAdapter(max_retries=retries)
session.mount("https://", adapter)

def get_all_users(endpoint):
    users = set()
    page = 1

    while True:
        try:
            r = session.get(
                f"{GITHUB_API}{endpoint}",
                params={"per_page": 100, "page": page},
                timeout=15
            )
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"[!] Network error: {e}")
            sys.exit(1)

        data = r.json()
        if not data:
            break

        users.update(user["login"] for user in data)
        page += 1
        time.sleep(0.3)  

    return users

def follow_user(username):
    r = session.put(
        f"{GITHUB_API}/user/following/{username}",
        timeout=10
    )
    return r.status_code == 204

def main():
    print("[*] Fetching followers...")
    followers = get_all_users(f"/users/{USERNAME}/followers")

    print("[*] Fetching following...")
    following = get_all_users(f"/users/{USERNAME}/following")

    not_followed_back = sorted(followers - following)

    if not not_followed_back:
        print("[✓] You already follow everyone who follows you.")
        return

    print("\nUsers you do NOT follow back:")
    for user in not_followed_back:
        print(f"  - {user}")

    choice = input(f"\nFollow all {len(not_followed_back)} users? (y/n): ").lower()
    if choice != "y":
        print("[!] Aborted.")
        return

    print("\n[*] Following users...")
    for user in not_followed_back:
        if follow_user(user):
            print(f"[+] Followed {user}")
        else:
            print(f"[!] Failed to follow {user}")

    print("\n[✓] Done.")

if __name__ == "__main__":
    main()
