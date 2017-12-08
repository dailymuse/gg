#!/usr/bin/env python3

# Some code based off of:
# - https://code.google.com/p/gource/wiki/GravatarExample
# - https://gist.github.com/macagua/5c2f5e4e38df92aae7fe

import getpass
import os
import subprocess
import hashlib
import urllib
from time import sleep, time

import requests

def md5_hex(text):
    m = hashlib.md5()
    m.update(text.encode("ascii", errors="ignore"))
    return m.hexdigest()

def get_gravatar_url(query, username, password):
    url = "https://api.github.com/search/users?utf8=%E2%9C%93&q={}&type=Users".format(urllib.parse.quote_plus(query))
    request = requests.get(url, auth=(username, password))

    if int(request.headers["X-RateLimit-Remaining"]) == 0:
        sleep_time = int(request.headers["X-RateLimit-Reset"]) - time() + 1

        if sleep_time > 0.0:
            sleep(sleep_time)

    response = request.json()
    items = response.get("items", [])
    return items[0]["avatar_url"] if items else None

def main():
    if "GITHUB_USERNAME" not in os.environ:
        print("`GITHUB_USERNAME` not set; skipping avatar fetch")
        return
    elif "GITHUB_PASSWORD" not in os.environ:
        print("`GITHUB_PASSWORD` not set; skipping avatar fetch")
        return

    username = os.environ["GITHUB_USERNAME"]
    password = os.environ["GITHUB_PASSWORD"]
    
    # Get the authors from the git log
    gitlog = subprocess.check_output(["git", "log", "--pretty=format:%ae|%an"], cwd="repo")
    authors = set(gitlog.decode("ascii", errors="ignore").splitlines())
    print("Users: ", authors)

    # Check each author
    for author in authors:
        # Get e-mail and name from log
        email, name = author.split("|")
        output_file = os.path.join("avatars", "{}.png".format(name))
        print("Checking {} <{}>".format(name, email))

        if os.path.exists(output_file):
            print("Image already cached")
            continue

        # Try to find the user on GitHub with the e-mail
        url = get_gravatar_url("{} in :email".format(email), username, password)

        if not url:
            # Try to find the user on GitHub with the name
            url = get_gravatar_url("{} in :name".format(name), username, password)

        if not url:
            # Eventually try to find the user with Gravatar
            url = "http://www.gravatar.com/avatar/" + md5_hex(email) + "?d=identicon&s=" + str(90)

        # Save the image
        if url:
            print("Avatar url: %s" % url)

            try:
                r = requests.get(url)

                if r.ok:
                    with open(output_file, "wb") as img:
                        img.write(r.content)
            except Exception as e:
                print("There was an error with %s <%s>: %s" % (name, email, e))

if __name__ == "__main__":
    main()
