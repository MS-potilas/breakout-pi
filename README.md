# Breakout 1976 (RetroPie Edition)

[![Language](https://img.shields.io/badge/language-python-blue.svg?style=flat)](https://www.python.org)
[![Module](https://img.shields.io/badge/module-pygame-brightgreen.svg?style=flat)](http://www.pygame.org/news.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](LICENSE)


## About

This project is a hardware-faithful Python and Pygame recreation of the original 1976 Atari **Breakout** arcade game. 

It was developed specifically with **RetroPie** and the **Raspberry Pi 4** in mind. Since the Raspberry Pi 4 cannot emulate the original game's complex Transistor-Transistor Logic (TTL) circuits via traditional emulators like MAME, this Python implementation serves as a lightweight alternative to bring the authentic arcade experience to the system. While optimized for RetroPie, it can easily be run on any standard desktop environment (Linux, macOS, Windows) either in a window or full-screen mode.

The game is designed to be highly faithful to its historic TTL predecessor, emulating original physics, brick layouts, and ball mechanics. However, a few modern enhancements and gameplay improvements have been introduced. For purists, these enhancements can be disabled entirely using command-line options.

## Features & Controls

### Authentic Gameplay, Flexible Display

Faithfully replicates the original 1976 speed, angles, and score mechanics. Use full-screen or windowed modes (normal, mini) via CLI options.

### Controls
*   **1, spacebar, mouse button, or joystick button:** Start a 1-player game.
*   **2:** Start a 2-player game.
*   **Spacebar, mouse button, or joystick button:** Launch ball
*   **Mouse / Keyboard (Arrow Keys):** Move the paddle left or right.
*   **Joystick:** Move the paddle left or right.
*   **P:** Pause the game (unless `--nopause` is used)
*   **F:** Toggle between Full FPS (game runs as fast as it can) and 60 FPS
*   **Esc:** Exit the game.

### Modern Enhancements

Subtle quality-of-life improvements (can be toggled off via CLI options).

*   New Happy End (remove using `--nohappyend`)
*   Mouse support
*   Serve Light implementation, visually subtle
*   Brick wall properly centered by moving the wall right by 2 pixels (remove using `--nowallshift`)
*   Text overlay which explain the single digit numbers (remove using `--notextoverlay`)
*   Sounds "tuned" to chromatic scale, default is major scale, but can be changed to minor, rock, blue, and pentatonic.
*   Mini (shrunk) version of the game
*   Paddle twice as wide as normal, if you wish.
*   Alternate bezel composed from real arcade bezel artwork
*   Full FPS Mode
*   AI Play Mode
*   Pause function (disable using `--nopause`)

## Screenshots

Click on any image to view it in full resolution.

<table align="center">
  <tr>
    <td align="center" width="50%">
      <b>Full Screen, Default Bezel, Game Paused</b><br>
      <a href="https://raw.githubusercontent.com/MS-potilas/breakout-pi/master/assets/full-screen.jpg"><img src="assets/full-screen.jpg" width="100%" alt="Full Screen with default bezel"></a>
    </td>
    <td align="center" width="50%">
      <b>Waiting for Serve (light is on)</b><br>
      <a href="https://raw.githubusercontent.com/MS-potilas/breakout-pi/master/assets/full-screen-waiting-for-serve.jpg"><img src="assets/full-screen-waiting-for-serve.jpg" width="100%" alt="Waiting for serve"></a>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <b>Full Screen, Alternate Bezel, Rainbow Colors</b><br><tt>--altbezel --altcolors</tt><br>
      <a href="https://raw.githubusercontent.com/MS-potilas/breakout-pi/master/assets/full-screen-altbezel-rainbowcolors.jpg"><img src="assets/full-screen-altbezel-rainbowcolors.jpg" width="100%" alt="Full Screen, Alternate Bezel, Rainbow Colors"></a>
    </td>
    <td align="center" width="50%">
      <b>Full Screen, No Bezel, No Overlay Tezt</b><br><tt>--nobezel --nooverlaytext</tt><br>
      <a href="https://raw.githubusercontent.com/MS-potilas/breakout-pi/master/assets/full-screen-no-bezel-no-overlaytext-mono.jpg"><img src="assets/full-screen-no-bezel-no-overlaytext-mono.jpg" width="100%" alt="Full Screen, No Bezel, No Overlay Tezt"></a>
    </td>
  <tr>
    <td align="center" width="50%">
      <b>Windowed, Rainbox Colors</b><br><tt>--altcolors</tt><br>
      <a href="https://raw.githubusercontent.com/MS-potilas/breakout-pi/master/assets/windowed-rainbowcolors.jpg"><img src="assets/windowed-rainbowcolors.jpg" width="50%" alt="Windowed, Rainbox Colors"></a>
    </td>
    <td align="center" width="50%">
      <b>Windowed, Mini</b><br><tt>--mini</tt><br>
      <a href="https://raw.githubusercontent.com/MS-potilas/breakout-pi/master/assets/windowed-mini.jpg"><img src="assets/windowed-mini.jpg" width="100%" alt="Windowed, Mini"></a>
    </td>
  </tr>

</table>

## Installation & Running

Follow these steps to get the game running on your system.

### Prerequisites

You will need **Python** (3.7.3 or newer) and **Pygame** (1.9.4 or newer) installed.

On Debian-based systems (such as Ubuntu or Raspberry Pi OS / RetroPie), install Pygame via apt:
```bash
sudo apt update
sudo apt install python3-pygame
```

### General Setup

1. **Clone the repository** and navigate to the project directory:
   ```bash
   git clone https://github.com/MS-potilas/breakout-pi.git
   cd breakout-pi
   ```

2. **Run the game**:
   ```bash
   python3 breakout.py
   ```

   You can any [command line options](#command-line-options) after breakout.py.

---

## Command-Line Options

You can customize the game mode and disable enhancements using the following flags:

| Option | Description |
| :--- | :--- |
| `‑‑fullscreen` | Opens the game in full-screen mode (default when run without a window manager). |
| `--windowed` | Opens the game in a windowed mode. |
| `--authentic` | Disables all modern enhancements and forces strict 1976 TTL-faithful rules. Implies `--nohappyend`, `--noservelight`, `--nowallshift`|
| `--nopause` | Pause not enabled. |
| `‑‑nohappyend` | Disables the better new ending and enables the original ending, where, after clearing the second wall, the player must lose all their balls before the game ends, which is somewhat depressing. In new, happy ending, the game ends when the last brick is destroyed, score and ball number stay on the screen. |
| `‑‑noservelight` | Do not show "SERVE"-light. |
| `‑‑nowallshift` | Do not shift brick wall 2 pixels right. 2 wall shift centers the wall, on original 1976 game it is not centered.|
| `--bigpaddle` | Tired of how hard the game is? Try this 2 x wider paddle option. The game is still hard to play through, but it is more possible than with the tiny default paddle. |
| `--mini` | The game shrunk 50% by width and height. Nice in window, for example. |
| `‑‑notextoverlay` | Disable "PLAYER UP" and  "BALL IN PLAY" overlay texts. You can use real text overlay on your monitor. |
| `--fullfps` | The game starts in full FPS mode. |
| `--aiplay` | AI plays the game. Tip: you can use arrow keys or joystick (but not mouse) to make AI miss the ball. |
| `‑‑nocolorstrips` or `‑‑nocolors` or `‑‑monochrome` or `‑‑mono` | No color strips, just black and white monitor. You can put real color strips on your monitor! |
| `--fontgap` | Move the single digits away from the wall. |
| `--nobezel` | Do not use bezel art. You can use real bezel around your monitor, if you want. |
| `--altbezel` | Use alternate bezel art. Cannot be used in fullscreen mode (which does not support bezels). |
| `‑‑rainbowcolors` or `‑‑altcolors` | Swap the green and yellow colors so that the colors are in the order of the rainbow. |


Sound scale options, default scale is major.

| Option | Description |
| :--- | :--- |
| `--minor` | Minor scale. |
| `--rock` | Rock scale. |
| `--blues` | Blues scale. |
| `--pentatonic or --penta` | Pentatonic scale. |


---

## RetroPie Integration

You can install this game into your RetroPie build either under the **Ports** menu or inside the **Arcade** system. In both methods, the core game files will reside in the `roms/ports/` directory.

### Method 1: Installation under "Ports" (Standard)

1. **Move the project folder** to your RetroPie roms directory:
   ```bash
   mv ../breakout-pi ~/RetroPie/roms/ports/breakout-pi
   ```

2. **Create a launch script** inside the ports directory:
   ```bash
   nano ~/RetroPie/roms/ports/Breakout.sh
   ```

3. **Paste the following content** into the file:
   ```bash
   #!/bin/bash
   python3 ~/RetroPie/roms/ports/breakout-pi/breakout.py
   ```

   (You can add [command line options](#command-line-options) after breakout.py)


4. **Make the script executable**:
   ```bash
   chmod +x ~/RetroPie/roms/ports/Breakout.sh
   ```

### Method 2: Optional Installation under "Arcade"

If you prefer to have Breakout listed alongside your other classic arcade games, you can register it as a custom "emulator":

1. Keep the game files in `~/RetroPie/roms/ports/breakout-pi` as shown in Method 1.
2. Remove the Ports launch script, create a dummy zip file in the arcade directory, and open the arcade emulator configuration:
   ```bash
   rm ~/RetroPie/roms/ports/Breakout.sh
   touch ~/RetroPie/roms/arcade/breakout.zip
   nano /opt/retropie/configs/arcade/emulators.cfg
   ```

3. **Add this line to the end of the file** (then save and exit):
   ```bash
   breakout-pi = "python3 ~/RetroPie/roms/ports/breakout-pi/breakout.py"
   ```

   (If you want, add [command line options](#command-line-options) between **breakout.py** and **"** to the line you add)

4. **Restart EmulationStation** (via Main Menu -> Quit -> Restart EmulationStation). A game named **breakout** will now appear under your *Arcade* system.

5. **Launch the game** from the Arcade menu. Press any key on your keyboard or controller during the launch screen to open the RetroPie Runcommand menu. Select **breakout-pi** as the default emulator for this specific game.

---

## Credits & Acknowledgements

*   **Codebase:** The initial gameplay framework was inspired by a tutorial repository by [codegiovanni](https://github.com/codegiovanni/Breakout). The code has since been roughly 90% rewritten, optimized, and expanded to implement hardware-accurate physics and RetroPie support.
*   **Graphics:** The 16:9 arcade bezel overlay is based on artwork from [The Bezel Project](https://github.com/thebezelproject/bezelproject-MAME). The original image was modified to remove transparency (replaced with a solid black background) and the arcade game instructions were edited to match this standalone implementation.

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
