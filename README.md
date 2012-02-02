Goose-In-Flask
==============

A simple Flask web service around excellent [Goose - Article Extractor](https://github.com/jiminoc/goose)

Installation
------------

It depends on Flask and JPype

Flask installation is fairly straightforward

    pip install flask

To install JPype you need to download it from SourceForge first
https://sourceforge.net/projects/jpype/files/

If you installing it on Mac OS X Lion, I would recommend to read this blog post
first http://blog.y3xz.com/post/5037243230/installing-jpype-on-mac-os-x

On Debian you can just type

    apt-get install python-jpype

To extract top image from the articles you will also need to have ImageMagic installed.

Getting started
---------------

Start an application

    python application.py

Then open your browser and type in:

    http://127.0.0.1:5000/?url=http://www.bbc.co.uk/news/science-environment-12275979

If top_image is always empty, make sure that CONVERT_PATH and IDENTIFY_PATH are
correct. To override them copy/rename "application.cfg.example" to
"application.cfg" and specify your own values.

Using latest version of Goose
-----------------------------

To use latest version of Goose you will need to complile it yourself using
Maven.

     git clone git://github.com/jiminoc/goose.git
     cd goose
     mvn package
     mvn dependency:copy-dependencies

Then copy "target/goose-<version>.jar" and all .jar files from
"target/dependency" folder to "goose-in-flask/build" folder.
