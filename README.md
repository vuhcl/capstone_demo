# Capstone Demo

Bipolar disorder, also known as manic-depressive illness, is a severe mental health condition characterized by recurrent episodes of mania or hypomania interspersed with episodes of depression (Anderson, Haddad, & Scott, 2012). It is among the top five most common mental illnesses in the US, affecting an estimated seven million people (2.8% of the adult population) (Kessler et al., 2004). Despite its pervasiveness, however, bipolar is usually misdiagnosed or only diagnosed after years of symptoms (Emilien, Septien, Brisard, Corruble, & Bourin, 2007). More importantly, various studies have found that there is low public awareness of the disorder, with incorrect beliefs that often indicate the stigma of bipolar (Durand-Zaleski, Scott, Rouillon, & Leboyer, 2012; Ruiz et al., 2012; Furnham & Anthony, 2009; Ellison, Mason, & Scior, 2013). To address this gap in public understanding of bipolar disorder, this Capstone project proposes and develops a realistic simulation of the disorder in the form of a visual novel that would help people recognize the wide spectrum of possible symptoms and know how to support someone with bipolar. The term visual novel here refers to an interactive game genre, featuring text-based story aided by static or sprite-based visuals. In this project, bipolar disorder is simulated using a Markov model, where the states are the mental states of the character (normal, manic, hypomanic, depressive, etc.) and the observable states are the variety of decisions available to the player.


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

## External Links
Distributions of the demo for Mac and Windows are available at: [Google Drive](https://drive.google.com/open?id=1L9z9K4uG5f1p2aC78p-NOf77vLd2NpN0)

