#!/bin/bash
echo "enter the username to scrape followers from:"
read username
echo "enter the name and/or path of the file to save found followers to:"
read filepath
gh api users/$username/followers --paginate | jq -r '.[].login' > $filepath
echo "all followers have been scraped from $username and saved to $filepath"
