#!/env/Python3.10.4
#/MobCat (2023)

import PySimpleGUI as GUI
import subprocess
import os
import sys
from sys import exit as exit
import shutil

# If you don't have PowerISO installed, then theres no point in running this scrupt
# This is also stupid, we should be abale to extract it our selves at worst
# at best, just read the xbe data from inside the xiso
if os.path.exists('C:/Program Files/PowerISO/piso.exe') == False:
    GUI.popup_error('You do not have PowerISO Installed\nIt is needed for this shitty program to function')
    exit(1)


# Hotfix for running the app from context menu
# AKA idk how to build a propper installer so I also don't know how to read a reg of where this was installed to
# Could just make a new reg for it but thats kinda messy and I dont think its the "right" way of doing that..
os.chdir('C:/XISOTools')

#################################
# Extract the xbe from the xiso #
#################################
# Get file path of the iso we just droped to this script
fi = sys.argv[1]
#fi = 'G:\\XISOs\\NTSC-U\\Genma Onimusha (USA)\\Genma Onimusha (USA).iso'
# Make a new string with just our iso file name.
strfi = str(fi).rsplit('\\', 1)[-1]

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
        GUI.popup_error(f'\n!!!ERROR!!!\n{strfi}\nis not an XISO or an xbox game!')
        fileHandle.close()# Python sometimes fails to flush/close so ALWAYS do it manually! see https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
        exit(1)
    input_file_size = fileHandle.seek(0,2)# sometimes the OS lies about the file size, esp Windows with compressed file sizes and such. Actually checking is usually best.
    fileHandle.close()

# Check file name length. It had something to do with 42 but don't remember which.
if len(strfi) > 42:
    GUI.popup_error(f'\n!!!ERROR!!!\n"{strfi}"\nThe FATX file system has a max character limit of 42 for each file\nPlease remove {len(strfi)-42} chars from your original filename.\n\nPress Error to exit.')
    exit(1)

# Maybe should also check the games folder char leng too. But not sure if necessary yet.
# Something like this if we dident chdir first.
# if len(os.path.basename(os.getcwd())) > 42: ???


# Pass our iso to power iso to extract the defult xbe.
# TODO: This is trash, we should just be able to peek into the xiso, then peek inside the default.xbe
# As we are only grabbing the title id and title name, we can do that "as a hex editor" you just have to flip some things around.
# See byte_offsets, but they wont be in the same location on a random xbe though.
subprocess.run(f'"C:/Program Files/PowerISO/piso.exe" extract "{fi}" /default.xbe -od "C:/XISOTools/tmp"', stdout=subprocess.DEVNULL)


#########################
# Extract info from xbe #
#########################
# This is stupid. Right now we are only ripping title id and name we should "just" do the reverse of editXBE, but the byte_offsets will be difrent for each XBE though..
# Use xbedump to rip cert as we dont have our own tool yet.
GetHeadder = subprocess.run(f"xbedump.exe tmp/default.xbe -dc", capture_output=True, text=True).stdout.strip("\t").splitlines()

# set values for Title ID and name
TitleID = GetHeadder[6][40:]
TitleName = GetHeadder[7][39:-1]

# Build a SN from our Title ID.
# Hex to ascii the frount half
SerialNumF = bytearray.fromhex(GetHeadder[6][40:-4]).decode()
# Hex to dec the back half to build our SN
SerialNum = f"{SerialNumF}-{str(int(GetHeadder[6][44:], 16)).zfill(3)}"

# Clean up the xbe now we dont need it.
os.remove("tmp/default.xbe")
       

#############################
# Edit data to make new xbe #
#############################
def editXBE(TitleID, TitleName):
    # Our big dumb list of where to manually edit the title id and title name into the attacher
    #               ID:4   ID:3   ID:2   ID:1   CH:1   0x00   CH:2   0x00   CH:3   0x00   CH:4   0x00   CH:5
    byte_offsets = [0x180, 0x181, 0x182, 0x183, 0x184, 0x185, 0x186, 0x187, 0x188, 0x189, 0x18A, 0x18B, 0x18C, 0x18D, 0x18E, 0x18F, 0x190, 0x191, 0x192, 0x193, 0x194, 0x195, 0x196, 0x197, 0x198, 0x199, 0x19A, 0x19B, 0x19C, 0x19D, 0x19E, 0x19F, 0x1A0, 0x1A1, 0x1A2, 0x1A3, 0x1A4, 0x1A5, 0x1A6, 0x1A7, 0x1A8, 0x1A9, 0x1AA, 0x1AB, 0x1AC, 0x1AD, 0x1AE, 0x1AF, 0x1B0, 0x1B1, 0x1B2, 0x1B3, 0x1B4, 0x1B5, 0x1B6, 0x1B7, 0x1B8, 0x1B9, 0x1BA, 0x1BB, 0x1BC, 0x1BD, 0x1BE, 0x1BF, 0x1C0, 0x1C1, 0x1C2, 0x1C3, 0x1C4, 0x1C5, 0x1C6, 0x1C7, 0x1C8, 0x1C9, 0x1CA, 0x1CB, 0x1CC, 0x1CD, 0x1CE, 0x1CF, 0x1D0] # This can go up to 0x20F but to lazy to do it right now. and not needed.
    # 81 len at 0x1D0
    # 81-4=77 77/2=38 max char lenth?

    # Sets up our list of edits to make then
    # split the TitleID into 2-character chunks and convert to byte values
    edits = []
    for i in range(0, len(TitleID), 2):
        hex_str = TitleID[i:i+2]
        byte_val = int(hex_str, 16)
        edits.append(byte_val)
    
    # flipts our list around
    edits.reverse()

    # Convert our TitleName into hex and space it out with 0x00
    # and chuck it onto the end of our lists of edits
    for i in range(len(TitleName)):
        hex_val = hex(ord(TitleName[i]))
        edits.append(int(hex_val[2:], 16))
        edits.append(0)

    # TODO:? Remove the extra 0x00 of the end of our edit list. But that would just give you and extra 1 char ontop of like 200, so it's fine for now
    #edits.pop([len(new_list)-1])

    # Now we have our edits to make, wrignt them to a new file
    with open("default.data", "rb") as f1, open("default.xbe", "wb") as f2:
        # Read the original contents of the file
        content = f1.read()

        # Modify the byte values at the specified byte_offsets
        # by enumrate over edits, using said edits at the byte_offsets
        for i, edit in enumerate(edits):
            content = bytearray(content)
            content[byte_offsets[i]] = edit

        # Write the modified contents to the new file
        f2.write(content)


#########################
#     Setup the GUI     #
#########################
# Main menu layout
layout = [
    [GUI.Text(f"Building attacher for")],
    [GUI.Text(f"{strfi}", font=('default', 10, 'bold'))], 
    [GUI.Text("If this info is correct, you can just press OK or Enter.\nOtherwise you can type a new name and press OK or Enter.\n")],
    [GUI.Text(f"TitleID:           {TitleID} | {SerialNum}")],
    [GUI.Text('Title Name: '), GUI.InputText(f'{TitleName}', key='input', enable_events=True, size=(40,1))],
    [GUI.Button("OK", key='btn_ok')]
    ]

# Create the window
window = GUI.Window("MobCat's trash tier XISO attacher builder v0.1", layout,
    default_element_size=(22, 1),
    return_keyboard_events=True,
    finalize=True)
    
window.TKroot.resizable(False, False)   # disable resizing of the window? X and Y?
#window.TKroot.attributes("-topmost", 1) # set the window to be always on top

# Remove the minimize and maximize buttons
# HOWEVER it also removes the window from the windows task bar. so it sucks, but it half works.
window.TKroot.attributes("-toolwindow", 1)

# Set the focus on the input element and all of it's text.
window['input'].Widget.select_range(0, len(TitleName))

##################################
# Run the GUI and get user input #
##################################
# This check should not go here...
CharLimit = 38
# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == GUI.WIN_CLOSED: # Just close the window.
        exit(1)
        #break
    elif event == 'btn_ok': # if the OK button in the window is pressed.
        #print(TitleID)
        #print(values['input'])
        #print(len(values['input']))
        # if the title name is longer then 38 char, fix it
        if len(values['input']) > CharLimit:
            values['input'] = values['input'][:CharLimit] 
            TitleName = values['input'][:CharLimit] 
            GUI.popup_error(f'Title too long! \nThe title name you entered was to long, so it has been truncated to {CharLimit} chractors for you')
            window['input'].update(value=values['input']) 
        else:
            editXBE(TitleID, values['input'])
            break

    elif event == '\r': # If the enter key is pressed.
        #print(TitleID)
        #print(values['input'])
        if len(values['input']) > CharLimit:
            values['input'] = values['input'][:CharLimit] 
            TitleName = values['input'][:CharLimit] 
            GUI.popup_error(f'Title too long! \nThe title name you entered was to long, so it has been truncated to {CharLimit} chractors for you')
            window['input'].update(value=values['input']) 
        else:
            editXBE(TitleID, values['input'])
            break


# Finlize and clean up now we have made our new xbe attacher
dir_path = os.path.dirname(fi)
shutil.copy("default.xbe", f'{dir_path}/')

# remove new xbe from attacher folder
os.remove("default.xbe")

window.close()