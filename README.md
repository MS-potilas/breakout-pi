# Breakout 1976 (RetroPie Edition)

[![Language](https://img.shields.io/badge/language-python-blue.svg?style=flat)](https://www.python.org)
[![Module](https://img.shields.io/badge/module-pygame-brightgreen.svg?style=flat)](http://www.pygame.org/news.html)
[![License](https://shields.io)](LICENSE)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](LICENSE)


## About

This project is a hardware-faithful Python and Pygame recreation of the original 1976 Atari **Breakout** arcade game. 

It was developed specifically with **RetroPie** and the **Raspberry Pi 4** in mind. Since the Raspberry Pi 4 cannot emulate the original game's complex Transistor-Transistor Logic (TTL) circuits via traditional emulators like MAME, this Python implementation serves as a lightweight alternative to bring the authentic arcade experience to the system. While optimized for RetroPie, it can easily be run on any standard desktop environment (Linux, macOS, Windows) either in a window or full-screen mode.

The game is designed to be highly faithful to its historic TTL predecessor, emulating original physics, brick layouts, and ball mechanics. However, a few modern enhancements and gameplay improvements have been introduced. For purists, these enhancements can be disabled entirely using command-line options.

## Features & Controls

*   **Authentic Gameplay:** Faithfully replicates the original 1976 speed, angles, and score mechanics.
*   **Modern Enhancements:** Subtle quality-of-life improvements (can be toggled off via CLI options).
*   **Flexible Display:** Seamlessly switches between full-screen and windowed modes.
*   **Controls:** 
    *   **Mouse / Keyboard (Arrow Keys):** Move the paddle left or right.
    *   **Joystick / D-Pad:** Full RetroPie controller support.
    *   **Esc / Q:** Exit the game.

## Screenshots

Click on any image to view it in full resolution.

<table align="center">
  <tr>
    <td align="center" width="50%">
      <b>Title Screen / Bezel View</b><br>
      <a href="https://githubusercontent.com"><img src="assets/screenshot1.jpg" width="100%" alt="Breakout Title Screen"></a>
    </td>
    <td align="center" width="50%">
      <b>Gameplay</b><br>
      <a href="https://githubusercontent.com"><img src="assets/screenshot2.jpg" width="100%" alt="Breakout Gameplay"></a>
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

---

## Command-Line Options

You can customize the game mode and disable enhancements using the following flags:

| Option | Description |
| :--- | :--- |
| `--fullscreen` | Opens the game in full-screen mode (default when run without a window manager). |
| `--windowed` | Opens the game in a windowed mode. |
| `--authentic` | Disables all modern enhancements and forces strict 1976 TTL-faithful rules. |


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
   cd "~/RetroPie/roms/ports/breakout-pi"
   python3 breakout.py
   ```

4. **Make the script executable**:
   ```bash
   chmod +x ~/RetroPie/roms/ports/Breakout.sh
   ```

### Method 2: Optional Installation under "Arcade"

If you prefer to have Breakout listed alongside your other classic arcade games:
1. Keep the game files in `~/RetroPie/roms/ports/breakout` as shown in Method 1.
2. Create the launch script inside your **arcade** roms folder instead:
   ```bash
   nano ~/RetroPie/roms/arcade/Breakout.sh
   ```
3. Paste the same launcher script text from Method 1 into this file and make it executable with `chmod +x`.

*After completing either method, restart EmulationStation to see the game appear in your chosen menu!*

---

## Credits & Acknowledgements

*   **Codebase:** The initial gameplay framework was inspired by a tutorial repository by [codegiovanni](https://github.com/codegiovanni/Breakout). The code has since been roughly 90% rewritten, optimized, and expanded to implement hardware-accurate physics and RetroPie support.
*   **Graphics:** The 16:9 arcade bezel overlay is based on artwork from [The Bezel Project](https://github.com/thebezelproject/bezelproject-MAME). The original image was modified to remove transparency (replaced with a solid black background) to fit this standalone implementation.

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
