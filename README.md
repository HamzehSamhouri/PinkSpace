![](./site_images/PinkSpace-header-image.png)

<!-- > Live demo [_here_](https://www.example.com). -->

## Table of Contents
* [General Information](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup and Usage](#setup-and-usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Contact](#contact)

## General Information
PinkSpace is a full-stack web application built using Python, Flask, MySQL, and Socket.IO. 

After registering an account users can create new posts, view and comment on posts from other users, as well as chat in real-time using the live-chat feature implemented utilizing socket.IO.

PinkSpace allows users to catch up with their friends without the toxic performative elements that tend to be associated with social media websites such as follower and/or like counts.

<br>




## Technologies Used
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [MySQL](https://www.mysql.com/)
* [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/)
* [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/1.0.1/)
* [Bootstrap](https://getbootstrap.com/)


<br>


## Features
- Login and registration with validation and Bcrypt for password security
- File upload for profile photos
- Posts and comments
- Profile page
- Global chat room

<br>


## Screenshots
Login and Registration page with designated validations 
![Login and Registration](./site_images/LoginandReg.png)

Main Homepage where users can create and respond to posts
![Homepage](./site_images/Homepage.png)

Followers page where users can follow and view other users' pages
![Followers](./site_images/Followers.png)

Real-time chat feature implemented using Socket.IO
![Chat](./site_images/Chat.png)

Edit your profile and upload a profile picture
![Edit Profile](./site_images/EditProfile.png)

<br>


## Setup and Usage
Project requirements/dependencies are located within Pipfile.lock file. 

        pipenv install 
        pipenv shell
        python3 server.py

<br>


## Project Status
Project MVP: _Complete_. However, additional features planned.

<br>

## Room for Improvement

Room for improvement:
- CSS Responsiveness
> Aesthetic design and ease of use across a variety of device screen sizes 
- CSS File Organization
> Potentially allocate a CSS file for each HTML template page
<br>


To do:
- Global and Following-only homepage toggle
- Optional photo upload element for posts
- Socket.IO _rooms_ to allow for direct messages as well as message retention when the page is reloaded or closed
- CSS responsiveness and dark and light mode toggle
- Inspired by MySpace, add your favorite song that plays upon opening your profile

<br>

## Contact
Created by [@HamzehSamhouri](https://www.linkedin.com/in/hamzehsamhouri/) - feel free to contact me!
