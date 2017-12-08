# Gource Generator (gg)

Generates gource videos like [this](https://www.youtube.com/watch?v=cNBtDstOTmA) for a github-based repos.

## Running it

Make sure you have these installed:

* [gource](http://gource.io/)
* [ffmpeg](https://www.ffmpeg.org/)
* python 3 + virtualenv

On mac with homebrew, you can install all of these via `brew install gource ffmpeg python3`.

Then run `REPO_URL=[your git repo URL] make`. Once completed, you'll have a video available at `./gource.mp4`.

## Environment variables

gg is configured through environment variables. The `REPO_URL` environment variable is the only required one; it's the URL to your git repo.

These environment variables are optional:

* `GITHUB_USERNAME` and `GITHUB_PASSWORD`, which specify your github credentials. If set, gg will attempt to get avatars for the authors.
* `SECONDS_PER_DAY`: How many seconds the video should have for each day.
