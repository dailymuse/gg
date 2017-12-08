run: init
	source venv/bin/activate && python gource_avatars.py
	cd themuse && gource -1280x720 --seconds-per-day 0.2 --user-image-dir .git/avatar -o ../gource.ppm
	ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i gource.ppm -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 gource.mp4

init: themuse venv

themuse:
	git clone git@github.com:dailymuse/themuse.git

venv:
	virtualenv -p python3 venv
	source venv/bin/activate && pip install requests
