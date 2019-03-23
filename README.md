# exifChall
CTF Challenge for BSIDESCTF 19

The application is a user based photo uploading application which proccesses the file as defined in views.py and renders the image and relevant details (exif data). The user has access to their own photo gallery and none other. Relies on Nginx for serving protected images based on user permission through the X-Accel-Redirect header.

## Worker (Victim)
The worker will run on file upload from the context of a signed in vulnerable user with the JWT token assigned.

## Admin Auth
An admin page will exist that relies on the utilization of a static JWT token.


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
```


## RUN

docker-compose build
docker-compose up

## Reset state
docker-compose down -v

## Solution

exif image polyglot steals cookie ->


Notes:

Block all external sources and inline via CSP

register -> login
User forced to input js into image polyglot
execute polygot:
bot visits their page
cookie gets stolen
bot closes connection after x seconds and before

part 2 -

user will retrieve jwt from part one.
jwt will have username and role - will be static cuz too much effort to make them dynamic
expose signing key or sign against remote file on the same domain
user changes role to admin -> signs key
gets flag on static page
