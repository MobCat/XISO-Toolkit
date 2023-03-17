# XISO-Toolkit

Xbox ISO tools for your windows context menu

![Menu](https://media.discordapp.net/attachments/1063759326340186172/1086128301002727464/image.png)

# **Please note:**

**This project is currently a proof of concept, work in progress, brute-forced with python.**  
There are still lots to do and maybe one day I'll re-right this hole thing into a nice and small C++ app, but until then, has bloat sorry.

# Features
### Build attacher
![Build](https://cdn.discordapp.com/attachments/1063759326340186172/1086199128800903179/image.png)<br>
This will build an attacher default.xbe for the xiso you selected.<br>
This is use to mount the iso to your xbox so you can play the xiso on real hardware.<br>
Please note: The title name only supports ASCII so if you want to change it to something else 
like, Halo 2 (JPN) so you can tell it apart from Halo 2 (MULTI) then you need to keep your names in ASCII.<br>
Also some titles don't have ASCII names and will show up weird when trying to make an attacher,
you can also use this tool to set the name to something not broken<br>
![Unicode will be the death of me](https://cdn.discordapp.com/attachments/1063759326340186172/1086201047950827530/image.png)<br>
Or just set the title name to what ever you like, it's your attacher, do what you want.<br>

### Split Lardge XISO
![Split](https://cdn.discordapp.com/attachments/1063759326340186172/1086203796725706853/image.png)<br>
The original xbox's HDD is formatted with a unique disk format called FATX, This format shares a lot of the same limitations as FAT32.<br>
One of those limitations is a maximum file size, in this case of 4092 MB. And there are like 20% of xbox games that are larger then this
So to get them onto a real xbox, we need to split the xiso into chunks that are smaller then that limitation.<br>
Then the attacher will mount the game.1.iso first, then mount the game.2.iso right after it. And the xbox is none the wiser it still looks like one big disk to it.
Please note though, this limitation and tool is only needed for running xisos on real hardware at the current time. if your running an emulator
you should be able to just mount the big xiso to it without any issues. Please don't split the xiso if you don't need to.<br>

As this process can take a min or so, we gave you some music to listen to \\^__^/ You can even set it to whatever you like as well.<br>
But if for some reason you're a buzzkill, you can turn the music off, check the note at the end of the how to build section.

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

Download this repo and unpack it to C:\XISOTools<br>
Run the `pip install -r requirements.txt` to install all the libs (But I think I messed that up, missing libs still?)<br>
place `xbedump.exe` and `extract-xiso.exe` in this dir<br>
Make a new blank tmp folder in the XISOTools folder<br>
Back in the XISOTools folder, Run the `BuildAttacher.bat` and `BuildSplitter.bat`<br>
Run the `ContextMenu.reg` to add the XISO Toolkit options to your context menu<br>
If you don't want music, edit the `Music.cfg` and change the first line to anything other then `True`, You can also just delete the `Music.cfg` file if your lazy and don't want music ever but thats kinda sad.<br>
If you do want music, edit the `Music.cfg`, make sure the first line is exactly `True` it is case sensitive.<br>
Then you can make a new music folder in the XISOTools like in the defult setting and put all your .xm and .mod files in there<br>
Or you can change this file path to where you keep your own tracker music on your computer<br>

You can also just run the installer from the release page if you trust me. That will install the pre-built exe files you need and setup your reg aswell.<br>
The installer is still a little trash, but again it works for now, but needs cleanup lator.
