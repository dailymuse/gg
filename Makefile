REPO_URL := $(or ${REPO_URL}, git@github.com:dailymuse/oz.git)
SECONDS_PER_DAY := $(or ${SECONDS_PER_DAY}, 1.0)

gource.mp4: gource.ppm
	ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i gource.ppm -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 gource.mp4

repo:
	git clone $(REPO_URL) repo

venv:
	virtualenv -p python3 venv
	source venv/bin/activate && pip install requests

avatars: venv
	mkdir -p avatars
	source venv/bin/activate && python avatars.py

gource.ppm: repo avatars
	cd repo && gource -1280x720 --seconds-per-day $(SECONDS_PER_DAY) --user-image-dir ../avatars -o ../gource.ppm

clean:
	rm -rf avatars repo venv gource.ppm gource.mp4
