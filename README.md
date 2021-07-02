# Pymunk Screensaver

Use this fun physics-based screensaver to bounce your friends' faces around your screen using the unstoppable logo/image of your choice!

## Installation

---

### Windows 10

- Install python 3.8+ (make sure to check 'Add python to PATH' option)
- Open a `new` PowerShell/Command Prompt window
  - Type `python -V` and press Enter
  - You should see `Python 3.X.X`. Anything else means something went wrong
- Clone/download this repo into `C:\pymunk-screensaver` (or the launcher won't work)
- In PowerShell/Command Prompt, run:
  - `cd C:\pymunk-screensaver`
  - `pip install -r .\requirements.txt`
  - `python .\main.py`
- To run as a screensaver, windows requires an executable with `.scr` extension:
  - I have written a very simple launcher that will run this screensaver
  - The `.cpp` file can be found in `.\launchers\win10` (you will need to compile it)
  - If you trust me, you can just use `.\launchers\win10\pymunk-screensaver-launcher.scr`
- Run the launcher to make sure it can start the screensaver
  - You will get a warning because Windows won't trust it
  - TODO: Explain how to handle the warning message
  - If the screensaver doesn't start, double-check the above steps
- Once you have confirmed the launcher starts copy the `.scr` file to `C:\Windows\SysWOW64`
- Open screensaver settings (click 'Start', type `screensaver`, and press Enter)
- If everything went well, you should see the launcher as an option in the dropdown
- `'Settings...'` and `'Preview'` will just launch the screensaver. Other than that, the rest of the settings should work.

## Customization

---

- To change the logo:
  - Overwrite `logo.png` in `C:\pymunk-screensaver\png\` with a similarly sized `.png` image.
- To change the faces:
  - Add or replace images in `C:\pymunk-screensaver\png\faces\` (Ideal size is close to 128x128).
- **Backgrounds must be transparent for the edge-detection to work right**
- If the collisions seem wrong, press `F1` while the screensaver is running to get a debug view of the collision object
- Delete the files in `C:\pymunk-screensaver\vertices\` to recalculate edges on next run

## Enjoy!
