# OhHiSolver

This program is used to solve OhHi puzzles.

[OhHi](https://play.google.com/store/apps/details?id=com.q42.ohhi&hl=en_US) is a zen style puzzle game developed by Q42.

This program includes three main components:

 * A class for solving the board
 * A wxPython GUI for playing with and testing the solver.
 * A program to connect to an android device through ADB to directly play the game on device.

## Usage

### GUI
The GUI can simply be executed in python with `python OhHi_GUI.py`.

### Phone Interaction
This program has only been tested on a Google Pixel 2 XL. The grid coordinates in would need to be changed to work on other sized displays.

```
python OhHi_Phone.py <grid_size> [<number_of_games>]
```
The grid size can only be one of 4, 6, 8, 10, and 12. If the number of games is not provided, this will play games until terminated.

Before being used on a phone, the phone must have [OhHi](https://play.google.com/store/apps/details?id=com.q42.ohhi&hl=en_US) installed and open. The game must also be 

## Dependencies

 * Numpy
 * wxPython
 * ADB (In PATH)
