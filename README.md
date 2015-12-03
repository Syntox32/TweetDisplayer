# TweetDisplayer

It's a thing that displays tweets on an Adafruit ![LCD thing](http://i.imgur.com/GFed4jp.png) because phones are too mainstream

## Usage

Configure the LCD pins on line 9 in `main.py` to your wiring setup.

Configure the `displayer.conf` file and put it in the `/etc/supervisor/conf.d/` directory.

Run `pip install -r requirements.txt`.

Run `sudo supervisorctl start displayer`.