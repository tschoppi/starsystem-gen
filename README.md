# GURPS 4<sup>th</sup> Edition Star System Generator


Welcome!

Here lives the automated star system generator for the GURPS Roleplaying
framework. I'm not far yet, but many features are to come.

## Table of Contents
 1. [About](#about)
 2. [Vision](#vision)
 3. [Features](#features)
 4. [Plans](#plans)
 5. [Contribute](#contribute)


## About
I really liked the way that GURPS Space allows for randomly generated worlds.
However, I wasn't very thrilled with the aspect of having to do all that work
manually over and over again for each new star system that I wanted to generate.

Since a computer is far better at performing such menial, low-level tasks than
a human, I decided to start scripting a random star system generator. Quickly I
realised that it would take more than a couple of scripts, but fully fledged OOP
programming to take on such a task. Thus the python-based Star System Generator
has come into existence.


## Vision
What I want is a tool that a GM can fire up in a matter of seconds, and that
results in a nicely formatted PDF document, from which then all the necessary
details can be gleaned to create an interesting game experience for all
participants.

This is aimed towards the gaming groups that play by a "let's embark on this
journey to a random location" kind of style.


## Features
The initial commit started with:
 - **GURPS Dice Roller**
 - **GURPS Star**, with
     * Mass
     * Spectral Type
 - **GURPS Star System**, with
     * Age
     * Location (e.g. are we in an open cluster or not)

And has now been expanded to include:
 - **GURPS Tables**, the file where all the tables will be stored in.


## Plans
Planned is the following:
 - Completion of the Star System Generation as described in the rulebook GURPS
   Space, available [here](http://www.warehouse23.com/products/SJG31-1002).
 - Making output to a LaTeX document available, for quick and easy generation of
   a Star System Dossier, containing tables with all information that might be
   relevant to the GM.
 - Eventually (read: far future) I want to bind in GURPS City Stats to work with
   this, so not only worlds and star systems are generated, but even contain
   cities and the like!


## Contribute
You may of course fork this project and make it better. Don't forget to phone
back home once in a while with a merge-pull request!
