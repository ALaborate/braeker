# braeker

This program is designed to serve as trigger that notifies the user 
that its time to stand up, leave workstation and have some rest.

Basic idea is that you print how many time you plan to work, console window disappears and shows up after the time passed.
If you need to interrupt program just run another instance.

Despite its writen in python, I make some library calls to show and hide console windows, so the progran is **Windows-only**.

### Examples of accepted inputs (no quotes)
"120" - 120 seconds  
"15m" - 15 minutes  
"2h" - 2 hours  
"q" - show stats and quit  
"?" - display help  

### Installation
1. Download and install latest python 3 release
1. Download file `braeker.py` from the repo and place it in any convenient folder
1. Optionally, download soundfile `brokenGlass.wav` to allow program make noisy sound on interruption. 
1. Optionally, make a shortcut
