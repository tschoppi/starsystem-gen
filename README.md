# GURPS 4<sup>th</sup> Edition Star System Generator

The code can be found on GitHub: http://github.com/tschoppi/starsystem-gen/

## What is this?

If you have never heard of the role-playing framework GURPS, check out the following link: http://www.sjgames.com/gurps/

This program was designed to assist the GM by quickly creating a random star system for his gaming group to explore, using the rulebook **GURPS _Space_**. It is primarily aimed at a GM with a group that is more of the adventurous type that travels a lot, but can also be used to generate a good base for a star system that will get details added manually later on.

**GURPS _Space_** is available here: http://www.sjgames.com/gurps/books/space/

## How do I use this?

### CLI Version
Basically, download the code and put it in a folder. Currently installing as a Python module onto the system is not supported, but will come in the future. Some day.

After that have a look at the `example.py` file and modify it to suit your needs. Currently not many options are available, but there will be more!

### Web Version
In v0.3 we introduced a web interface which is self-hosting, meaning that all the work is done locally on your machine. From the root directory start the server with the command

    python3 server.py

Python 3.5 changed the way arguments are handled, breaking our code. We're investigating why PEP448 affects us, but it is low priority,
since Python 3.4 is often still available and our code works with it.
One of our features is only supported on Chrome, as no other browser yet supports the Canvas2D.Ellipse.

If they are not already on your system, you need to install the 3<sup>rd</sup> party modules `cherrypy` and `jinja2`.
An easy way to do that is with pip3:

    pip3 install cherrypy jinja2


When the server is up and running, open your favorite browser and navigate to `localhost:8080` where you can interact with the software.


## I found a bug!

If you found something that is not working as it should, please report it in the *issues* section here: http://github.com/tschoppi/starsystem-gen/issues
