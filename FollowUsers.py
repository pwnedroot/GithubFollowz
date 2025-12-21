import requests
import time

# Replace with your personal access token
TOKEN = "Your_Github_Access_Token_Here"

# File containing GitHub usernames, one per line
USER_FILE = "usernames.txt"

# Time to wait between follow requests (in seconds)
DELAY = 10  

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def follow_user(username):
    url = f"https://api.github.com/user/following/{username}"
    response = requests.put(url, headers=headers)
    if response.status_code == 204:
        print(f"Successfully followed {username}")
    elif response.status_code == 404:
        print(f"User {username} not found")
    else:
        print(f" Failed to follow {username}: {response.status_code}, {response.text}")

def main():
    with open(USER_FILE, "r") as f:
        users = [line.strip() for line in f if line.strip()]

    print(f"Starting to follow {len(users)} users...")

    for username in users:
        follow_user(username)
        time.sleep(DELAY)  # wait to avoid abuse detection

if __name__ == "__main__":
    main()
