#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Based on:
# - https://code.google.com/p/gource/wiki/GravatarExample
# - https://gist.github.com/macagua/5c2f5e4e38df92aae7fe
#
# Get list of authors + email with git log
# git log --format='%aN|%aE' | sort -u

import getpass
import os
import subprocess
import hashlib
from time import sleep, time

import requests

def md5_hex(text):
    m = hashlib.md5()
    m.update(text.encode('ascii', errors='ignore'))
    return m.hexdigest()

def get_data(url):
    r = requests.get(url, auth=(username, password))

    if int(r.headers["X-RateLimit-Remaining"]) == 0:
        sleep_time = int(r.headers["X-RateLimit-Reset"]) - time() + 1

        if sleep_time > 0.0:
            sleep(sleep_time)

    return r.json()

def get_avatar_from_github(url):
    data = get_data(url)
    items = data.get("items", [])
    return items[0]["avatar_url"] if items else None

def try_to_get_image_for_author(author, output_dir):
    # Get e-mail and name from log
    email, name = author.split('|')
    output_file = os.path.join(output_dir, '%s.png' % name)
    print("Checking %s <%s>" % (name, email))

    if os.path.exists(output_file):
        print("Image already cached")
        return

    url = None

    # Try to find the user on GitHub with the e-mail
    url = get_avatar_from_github("https://api.github.com/search/users?utf8=%E2%9C%93&q=" + email + "+in%3Aemail&type=Users")

    if not url:
        # Try to find the user on GitHub with the name
        url = get_avatar_from_github("https://api.github.com/search/users?utf8=%E2%9C%93&q=" + name + "+in%3Aname&type=Users")

    if not url:
        # Eventually try to find the user with Gravatar
        url = "http://www.gravatar.com/avatar/" + md5_hex(email) + "?d=identicon&s=" + str(90)

    # Save the image
    if url:
        print("Avatar url: %s" % url)

        try:
            r = requests.get(url)

            if r.ok:
                with open(output_file, 'wb') as img:
                    img.write(r.content)
        except Exception as e:
            print("There was an error with %s <%s>: %s" % (name, email, e))

if __name__ == "__main__":
    global username
    global password

    # Login to the GitHub API
    username = input("Enter your GitHub username: ")
    password = getpass.getpass("Enter your GitHub password: ")

    # Configure the path of the git project
    base_dir = os.path.join(os.getcwd(), 'themuse')
    git_path = os.path.join(base_dir, '.git')
    output_dir = os.path.join(git_path, 'avatar')

    # Create the folder for storing the images. It's in the .git folder, so it won't be tracked by git
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the authors from the git log
    gitlog = subprocess.check_output(
            ['git', 'log', '--pretty=format:%ae|%an'], cwd=base_dir)
    authors = set(gitlog.decode('ascii', errors='ignore').splitlines())
    print("Users: ", authors)

    # Check each author
    for author in authors:
        try_to_get_image_for_author(author, output_dir)
