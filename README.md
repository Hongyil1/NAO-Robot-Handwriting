# NAO-Robot-Handwriting
This software builds up a human-robot interaction system. The user can teach the NAO Robot to write by writing in the pen-tablet. A Q-learning algorithm is used to help robot learn the hand-writing letter. There are three modes for users to use:
* Kinematic: Mimicking the writing trajectory through Kinematic
* Q-learning: Using Q-learning algoritm to learn the write actions
* Keyboard Control: Use keyboard to control Robot's right arm to write

![test1](https://user-images.githubusercontent.com/22671087/40587069-e0259240-620d-11e8-9812-7054dd4b8272.jpg)
## Prerequisites
* Python2.7
* NAO Robot
* Wacom Intuos (CTH-480) pen-tablet
* pynaoqi
* pygame
* Tkinter

## How to use
```
python Main.py -ip your_ip -port your_port
```
## Authors

* **[Hongyi Lin](https://github.com/Hongyil1)** 

## License

This project is licensed under the MIT License

## Demo
The Demo of Q-learning

<a href="https://imgflip.com/gif/2b3en1"><img src="https://i.imgflip.com/2b3en1.gif" title="made at imgflip.com"/></a>
