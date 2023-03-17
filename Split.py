#!/env/Python3.10.4
#/MobCat (2023)

import os
from tqdm import tqdm
from sys import argv
from sys import exit as exit
from random import choice
from time import sleep


"""
Changes: parzival
- Added XISO detection
- Python's native `exit()` isn't great, use `sys.exit()` to pass error codes
- `sys.pathsep` gives the right path separator for the OS
- optimized imports
- fixed possible data corruption issues
- reworked file read/write (Python's native "streaming" mode is kinda trash)
- added tqdm for free because of reworked file loop
"""
"""
Changes: MobCat
- Added back in the strfiShort var to clean up console output.
- Music folder can now be set from Music.cfg. User can also disable music from the cfg aswell.
- Added some ver info and cleaned up the console output to make it look "nicer"
- Fixed the 42 char lenth check as it was checking the hole file path, not just the file name.
- ASCII ART \^__^/
"""

#music_dir = 'C:/XISOTools/music/'
#music_dir = '/home/parzival/Music/MODs/'# if you're curious, mostly Amiga stuff.
# Now the user can set a folder if they like
# We probs should check if the file exists and make it if it doesn't but now we are nit picking.
# Also hard coded file paths are kinda stupid buuut I'm not doing the installer thing correctly so can't fix it right now.
if os.path.exists('C:/XISOTools/Music.cfg'):
    print('Loading Music.cfg')
    with open('C:/XISOTools/Music.cfg', 'r') as f:
        enableMusic = f.readline().strip('\n')
        music_dir = f.readline()
        f.close()
else:
    print(f'Music.cfg is missing or corrupted!')
    enableMusic = 'False' # Just setting this for safety..


# idk if you can do this, but ima try..
# And once we axe pygame just leaving pymod on all the time should not be an issue.
if enableMusic == 'True':
    from pygame import mixer # only import the music player as thats all we need.
    #from pymod import modplay # I tryed :'(
else:
    print(f'Music has been disabled, please check your Music.cfg')


chunk_size = 4092 * 1024 * 1024 # 4092 MB in bytes, limit is 4096, wanted to cut it at 4095 but I think 92 is safer.

# Get file path of the iso we just dropped to this script
fi = argv[1]
# Make a new string with just our iso file name.
if os.pathsep in fi:# not necessarily in a different folder than the XISO
    strfi = str(fi).rsplit(os.pathsep, 1)[-1]
    # Get path to change into, and change there.
    CurrentDIR = os.path.dirname(fi)
    os.chdir(CurrentDIR)
else:
    strfi = str(fi)

# make a new string with just our iso file name.
# Used to check the name len for FATX and make easer to read console outputs
strfiShort = str(fi).rsplit('\\', 1)[-1]


# ensure xiso, per extract-xiso
# https://github.com/XboxDev/extract-xiso/blob/3438285c5098757b112215c131e837876b566d31/extract-xiso.c#L457-L468
with open(str(fi), 'rb', buffering = 0) as fileHandle:# 'buffered=0' streams the file. that's the only difference.
    fileHandle.seek(31337)# we have to split the checks up because seek() returns the actual position... or 0, if it feels like it?
    isXISO = False
    if fileHandle.read(8) == b'in!xiso!':
        isXISO = True
    fileHandle.seek(0x10000)
    if fileHandle.read(20) == b'MICROSOFT*XBOX*MEDIA':# is this jank? yes. is there a better way to handle it? not really.
        isXISO = True
    if not isXISO:
        print(f'\n!!!ERROR!!!\n{strfiShort} is not an XISO!')
        fileHandle.close()# Python sometimes fails to flush/close so ALWAYS do it manually! see https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
        exit(1)
    input_file_size = fileHandle.seek(0,2)# sometimes the OS lies about the file size, esp Windows with compressed file sizes and such. Actually checking is usually best.
    fileHandle.close()

# Check If file even needs to be split in the first place
if not int(input_file_size)/1024/1024 > 4096:
    input(f'\n!!!ERROR!!!\n{strfiShort} ({round(int(input_file_size)/1024/1024, 2)} MB) is not lardger then 4096MB.\nThere is no need to split this file.\n\nPress Enter to exit.')
    exit()

# Check if split file exists.
#print(os.getcwd())
if os.path.exists(f'{fi[:-4]}.1.iso'):
    print(f'\n!!!ERROR!!!\nFile "{strfiShort[:-4]}.1.iso" ')
    if os.path.exists(f'{fi[:-4]}.2.iso'):
        print(f'and "{strfiShort[:-4]}.2.iso" ')
    print('Already exists. Please delete the old split and try again\n\nPress Enter to exit.')
    input()
    exit()
# This should only trigger if you pasted the .1.iso check but not .2.iso
if os.path.exists(f'{fi[:-4]}.2.iso'):
    input("You need to delete both halves of the split..\n\nPress Enter to exit.")
    exit()

# Check file name length. It had something to do with 42 but don't remember which.
if len(f'{strfiShort[:-4]}.1.iso') > 42:
    input(f'\n!!!ERROR!!!\n"{strfiShort[:-4]}.1.iso"\nThe FATX file system has a max character limit of 42 for each file\nPlease remove {len(strfiShort[:-4])+6-42} chars from your original filename.\n\nPress Enter to exit.')
    exit()

# if resulting file path would be to long?
# Not sure if I need to check for this
#setchar = f'F/Games/{os.path.basename(os.getcwd())}/{strfi[:-4]}.1.iso'

# Check for invalid chars in file name?? But I think FATX shares most of the same limits as windows does
# if char not in [ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&'()-.@[]^_`{}~ ](that includes space at the end)

# Calculate the number of chunks we need to split the file into
num_chunks = input_file_size // chunk_size + (1 if input_file_size % chunk_size > 0 else 0)

# Now all the checks are done. Start the music.
# TODO: Replace this with pymod so we don't need to include stuff we are not using like SDL
if enableMusic == 'True':
    mixer.init()
    # Build a list of music
    funkeyBeats = os.listdir(str(music_dir))
    # Play our random song.
    try:
        song = choice(funkeyBeats)
        
        #songfile = pm.load_file(str(music_dir)+song)
        #pm.play(songfile)
        mixer.music.load(str(music_dir)+song)
        mixer.music.play(-1)
        print(f'Now playing: {song}')
    except IndexError:
        print(f'{music_dir} Has no valid music.')
    

print(f'''
                                                           __
                                                         .' _| ⌐¬
 ▄▄   ▄▄ ▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄     /  /:\ \ \▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄   
█  █▄█  █   █       █       █  █       █       █   █   █| ::::\_\ \  █       █       █   ▄▄  █  
█       █   █  ▄▄▄▄▄█   ▄   █  █  ▄▄▄▄▄█    ▄  █   █   █\ \::::< _ _\█▄     ▄█    ▄▄▄█  █  █  █  
█       █   █ █▄▄▄▄▄█  █ █  █  █ █▄▄▄▄▄█   █▄█ █   █   █ \ \::::\ \ \  █   █ █   █▄▄▄█  █▄█▄▄█▄ 
 █     ██   █▄▄▄▄▄  █  █▄█  █  █▄▄▄▄▄  █    ▄▄▄█   █▄▄▄█  \█'.::.\ \ \ █   █ █    ▄▄▄█    ▄▄  █
█   ▄   █   █▄▄▄▄▄█ █       █   ▄▄▄▄▄█ █   █   █       █   █'-.__/  \ \    █ █   █▄▄▄█   █  █ █
█▄▄█ █▄▄█▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█  █▄▄▄▄▄▄▄█▄▄▄█   █▄▄▄▄▄▄▄█▄▄▄█    █▄▄▄ \ \▄▄▄█ █▄▄▄▄▄▄▄█▄▄▄█  █▄█
XISO Splitter v0.2 (20230317)  MobCat and Parzival Wolfram            \ \                      
                                                                       \_)                     ''')


# Open the input file for reading
with open(strfi, 'rb', buffering = 0) as f_in:
    # Get the file size in bytes
    # As we are not loading the whole ass iso into ram anymore we don't need a message for it.
    #print(f'loading "{strfiShort}" into memory, please wait...')
    #file_size = input_file_size# already did this
    
    # Loop through the input file and write to the output files

    # had to redo this, python's streaming method doesn't work with chunks >2GB and it's easier to do it ourselves anyway
    # there's also a fun Windows-only bug where SOMETIMES python's read buffer never, ever clears until you close the file,
    # so we have to use BOTH Python's native streaming system AND our own here!

    chunk_split_size = 32768# TODO: can we get destination cluster size or some shit like that without admin?
    total_count = input_file_size / chunk_split_size# breaking up reads into small chunks because streaming only allows up to 2GB per read, which also isn't ideal... and is undocumented?
    if int(total_count) != total_count:
        total_count = int(total_count) + 1# quick and dirty "do we need an extra read?" check
    for i in range(num_chunks):
        # this string cast seems weird but it's a little bit of shenanigannery with the underlying C, overcasting can sometimes be much faster for multiple reasons
        filenameOut = str(strfi[:-4] + '.' + str(i+1) + '.iso')
        print(f'\nWriting {strfiShort[:-4]}.{str(i+1)}.iso...') # Sorry, it just reads nicer in console.
        f_out = open(filenameOut,'wb')# not using with here because it tested slightly faster per read/write without it in isolated tests.
        for i in tqdm(range(chunk_size // chunk_split_size)):
            f_out.write(f_in.read(chunk_split_size))
            f_out.flush()
        f_out.close()
        
        

print('\nDone \\^__^/')
if enableMusic == 'True':
    mixer.music.fadeout(6000)
    #pm.fadeout(6000)
    sleep(6) # Have to wait for the fadeout otherwise mixer.quit() just kills it.
    mixer.quit()            
