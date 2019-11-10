# Capstone Demo
---
## Directory Guide

**Files and folders of interest:**

- /images: Folder storing image assets used in the game. Does not contain GUI files, which come with Ren'Py and are stored in /gui
- /baseobject.rpy: Script file containing code for the base model for character stats (currently unused in the game).
- /model.rpy: Script file containing code for the simulation model. Have some minor differences from the version submitted as Final Project for CS166, which includes:
  + Name changes of functions and variables to include a single leading underscore to signify internal (private) use of the object class according to PEP8.
  + Addition of methods for outward interface (call for update and access to model state from the game).
  + Removal of NumPy and Scipy dependencies due to issues in Ren'Py.
 - /random_choice.rpy: Scripting file containing code for weighted random sampling and sampling from a pseudo-continuous skew normal distribution.
 - /script.rpy: Main scripting file with initialization and scenes in the game. In the future when the game is further developed to have a much longer script, we will split up the scenes and store them in different files.
 
 Each of these script files have an identically-named .rpyc file, which contains compiled Python code from the corresponding .rpy file. These files are intended to obfuscate the plain text code written in .rpy files so that the .rpc files can be excluded from distributions, which the users have access to.
 
 ## Credits
Made with [Ren'Py](https://www.renpy.org/) 7.3.5.606.
 
Backgrounds by Uncle Mugen, made available in public domain under CC0

Character sprites by [Studio Senpai](https://studiosenpaigames.wixsite.com/studiosenpaigames), made available under license CC BY-NC 3.0

