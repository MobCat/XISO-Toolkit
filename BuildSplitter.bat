::pip install pyinstaller
::pip install pynput==1.6.8
::Have to recompile the hole fucking bootloader because windows 10 is a dick
:: https://stackoverflow.com/questions/43777106/program-made-with-pyinstaller-now-seen-as-a-trojan-horse-by-avg
:: https://pyinstaller.readthedocs.io/en/stable/bootloader-building.html

del Split.exe
mkdir Build
copy Split.py Build\
cd Build
pyinstaller -F Split.py
cd ..
copy Build\dist\Split.exe .
RD /S /Q Build
::pause