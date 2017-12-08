# Gource Generator (gg)

Generates gource videos like [this](https://www.youtube.com/watch?v=cNBtDstOTmA) for a github-based repos.

## Running it

Make sure you have [gource](http://gource.io/) and [ffmpeg](https://www.ffmpeg.org/) installed. On mac with homebrew, you can run `brew install gource ffmpeg`.

Then run `REPO_URL=[your git repo URL] make`. Once completed, you'll have a video available at `./gource.mp4`.

## Environment variables

gg is configured through environment variables. The `REPO_URL` environment variable is the only required one; it's the URL to your git repo.

These environment variables are optional:

* `GITHUB_USERNAME` and `GITHUB_PASSWORD`, which specify your github credentials. If set, gg will attempt to get avatars for the authors.
* `SECONDS_PER_DAY`: How many seconds the video should have for each day.
