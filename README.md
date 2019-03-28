# exifChall
CTF Challenge for BSIDESCTF 19

The application is a user based photo uploading application which proccesses the file as defined in views.py and renders the image and relevant details (exif data). The user has access to their own photo gallery and none other. Relies on Nginx for serving protected images based on user permission through the X-Accel-Redirect header.

<strong>Attackers will need a controlled site to obtain information from their xss payload</strong>

## Worker (Victim)
The worker will run on image save, the signal on the images model will send the filename and user id to the victim rabbitmq queue and the spawn process for the bot will listen to the queue and utilize selenium and phantomjs to navigate to the page. Bot proccess is currently spawned from django settings.py with subprocess.

## Admin Auth
An admin page will exist that relies on the utilization of a static JWT token. The token relies on signing from a resource available from the webserver, easiest resource is w3.css. The attacker then assigns their role to admin and goes to the admin page to get the flag.


## Issues

charset="ISO-8859-1" required if the .jpg extension is not on the loaded script.


------
Static Contents hosted on /nginx/static/*
Media contents hosted on shared volume.


OS Reqs
```
Docker
Docker-compose
```

Python Requirements
```
Pillow
Django==2.1.4
ExifRead==2.1.2
python-jose==3.0.1
gunicorn= "==19.9.0"
psycopg2
pika
selenium
```

## Setup
Modify the compose file's env variable to your need, if you change creds for prebuilt user it will need to be propogated to bot.

Be sure to modify settings.py to update allowed_hosts from wildcard if possible.

Modify APPROVED_SIGNER to external ip/hostname of the nginx instance.



## RUN

docker-compose build

docker-compose up

## Reset state
docker-compose down -v

## Solution

exif image polyglot steals cookie ->


Notes:

register -> login
User forced to input js into image polyglot
execute polygot:
bot visits their page
cookie gets stolen

part 2 -

user will retrieve jwt from part one.
jwt will have username and role - will be static cuz too much effort to make them dynamic
sign against a file contents on the server that the bot has access to.
user changes role to admin -> signs
gets flag on static admin page

## Flags
 SUN{why_bo0ther_with_ex1f}
 SUN{Can_Y0U_smell_JWT?}
