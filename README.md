# Pymunk Screensaver

Use this fun physics-based screensaver to bounce your friends' faces around your screen using the unstoppable logo/image of your choice!

[![Watch](https://github.com/davidecotten/pymunk-screensaver/blob/main/youtube.png)](https://www.youtube.com/watch?v=xpsSD27zrj4)

## Installation

### Windows 10

-   Install python 3.8+ (make sure to check 'Add python to PATH' option)
-   Open a `new` PowerShell/Command Prompt window
    -   Type `python -V` and press Enter
    -   You should see `Python 3.X.X`. Anything else means something went wrong
-   Clone/download this repo into `C:\pymunk-screensaver` (or the launcher won't work)
-   In PowerShell/Command Prompt, run:
    -   `cd C:\pymunk-screensaver`
    -   `pip install -r .\requirements.txt`
    -   `python .\main.py`
-   To run as a screensaver, windows requires an executable with `.scr` extension:
    -   I have written a very simple launcher that will run this screensaver
    -   The `.cpp` file can be found in `.\launchers\win10` (you will need to compile it)
    -   If you trust me, you can just use `.\launchers\win10\pymunk-screensaver-launcher.scr`
-   Run the launcher to make sure it can start the screensaver
    -   You may get a warning because Windows won't trust it:
        -   Click 'More info'
        -   Click "Run anyway'
    -   If the screensaver doesn't start, double-check the above steps
-   Once you have confirmed the launcher starts copy the `.scr` file to `C:\Windows\SysWOW64`
-   Open screensaver settings (click 'Start', type `screensaver`, and press Enter)
-   If everything went well, you should see the launcher as an option in the dropdown
-   `'Settings...'` and `'Preview'` will just launch the screensaver. Other than that, the rest of the settings should work.

## Customization

-   To change the logo:
    -   Overwrite `logo.png` in `C:\pymunk-screensaver\png\` with a similarly sized `.png` image.
-   To change the faces:
    -   Add or replace images in `C:\pymunk-screensaver\png\faces\` (Ideal size is close to 128x128).
-   **Backgrounds must be transparent for the edge-detection to work right**
-   To mess with the physics:
    -   At the top of `./main.py`, there are some constants defined. Feel free to modify them to see what happens.
-   If the collisions seem wrong, press `F1` while the screensaver is running to get a debug view of the collision object
-   By default, the collision vertices are recalculated each run. To start up faster, you can change the `RECALCULATE` constant.

## Enjoy!
