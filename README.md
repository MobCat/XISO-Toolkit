# XISO-Toolkit

Xbox ISO tools for your windows context menu

![Menu](https://media.discordapp.net/attachments/1063759326340186172/1086128301002727464/image.png)

# **Please note:**

**This project is currently a proof of concept, work in progress, brute-forced with python.**  
There are still lots to do and maybe one day I'll re-right this hole thing into a nice and small C++ app, but until then, has bloat sorry.

# #TODO:

The "splitter" script has some things to clean up with the music player, but otherwise I'm happy with it.  
The "build" script is a total dumpster fire. It works but it needs way to many pre-requirements, mainly PowerISO which is stupid, but idk how to raw read an xiso just to pull one file.  
And even then we don't need to pull one file, we just need to load that file to extract a few bits of info out of it. It's a mess.. Again I have no idea what I'm doing it and just brute-forcing it because nobody else is doing it in a way I like.
Allow for the user to actually select where they want the toolkit to be installed instead of forcing C:\XISOTools\

# Pre-requirements

**PEALSE NOTE:** None of these pre-requirements except for one will be needed as soon as I fix the attacher builder.  
PowerISO - For extracting the default.xbe from the XISO  
xbedump - For extracting title info from the default.xbe. This is super temporary, I should be able to work on this next.  
[Extract-xiso](https://github.com/XboxDev/extract-xiso)\- For rebuilding a Redump ISO into and XISO we can actually use.  
PLEASE NOTE AGAIN: By defult in this toolkit, extract-xiso WILL DELETE your redump when its done with the rebuild. I have not set a "user setting" for this.

# How to build (Temp)

Download this repo and unpack it to C:\XISOTools
Run the `pip install -r requirements.txt` to install all the libs (But I think I messed that up, missing libs still?)
place `xbedump.exe` and `extract-xiso.exe` in this dir
Make a new blank tmp folder in the XISOTools folder
Back in the XISOTools folder, Run the `BuildAttacher.bat` and `BuildSplitter.bat`
Run the `ContextMenu.reg` to add the XISO Toolkit options to your context menu
If you don't want music, edit the `Music.cfg` and change the first line to anything other then `True`, You can also just delete the `Music.cfg` file if your lazy and don't want music ever but thats kinda sad.
If you do want music, edit the `Music.cfg`, make sure the first line is exactly `True` it is case sensitive.
Then you can make a new music folder in the XISOTools like in the defult setting and put all your .xm and .mod files in there
Or you can change this file path to where you keep your own tracker music on your computer

You can also just run the installer from the release page if you trust me. That will install the pre-built exe files you need and setup your reg aswell.
The installer is still a little trash, but again it works for now, but needs cleanup lator.
