import numpy as np
import OhHiGame
#import os
import io # For io.BytesIO
import subprocess
import sys, time
from telnetlib import Telnet
from signal import *
from PIL import Image

#path = "/tmp/test.png"

size = 4
if(len(sys.argv) >= 2):
    size = int(sys.argv[1])

gamesToPlay = 0
playForever = True
gamesPlayed = 0

if(len(sys.argv) >= 3):
    gamesToPlay = int(sys.argv[2])
    playForever = False

top_left = [60, 800]
bottom_right = [1390, 2120]

grid_size = [bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]]

xoffset = (grid_size[0] / size) 
yoffset = (grid_size[1] / size) 

x_axis = [int((top_left[0] + xoffset/2) + xoffset * x) for x in range(size) ]
y_axis = [int((top_left[1] + yoffset/2) + yoffset * y) for y in range(size) ]

board = np.full([size, size], OhHiGame.NONE)

game_start_loc = [[480, 1300],[740,1300],[1000,1300],[480,1600],[740,1600]]

start_delay_size = [0.2, 0.25, 0.25, 0.4, 0.5]

game_x = game_start_loc[int((size - 4)/2)][0]
game_y = game_start_loc[int((size - 4)/2)][1]
start_delay = start_delay_size[int((size - 4)/2)]

monkey_proc = subprocess.Popen(["adb", "shell", "monkey -p \"com.q42.ohhi\" --port 1080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(["adb", "forward", "tcp:1080", "tcp:1080"], stdout=subprocess.DEVNULL)

time.sleep(1)

tn = Telnet("localhost", 1080)

starttime = time.time()

def clean(*args):
    print("\nCompleted")
    # Clean up
    tn.close()
    monkey_proc.kill()
    subprocess.run(["adb", "forward", "--remove", "tcp:1080"], stdout=subprocess.DEVNULL)
    subprocess.run(["adb", "shell", "kill $(pgrep monkey)"], stdout=subprocess.DEVNULL)

    e = int(time.time() - starttime)

    print("Games Played: %d" % gamesPlayed)
    print("Time Elapsed: %s" % '{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))
    sys.exit(0)

for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, clean)


time.sleep(1)

while(playForever or gamesToPlay > 0):

    tn.write(("tap %d %d\n" % (game_x, game_y)).encode())

    time.sleep(start_delay)

    image_bytes = subprocess.check_output(["adb", "shell", "screencap", "-p"])

    img = Image.open(io.BytesIO(image_bytes))
    im_px = img.load()

    for x in range(size):
        y_pix = y_axis[x]
        for y in range(size):
            x_pix = x_axis[y]

            pix_val = [ im_px[x_pix,y_pix][i] for i in range(3) ]

            average = sum(pix_val) / 3

            pix = [ val / average for val in pix_val ]

            if(pix[0] > (pix[2] + 0.2)):
                board[x,y] = OhHiGame.RED
            elif(pix[2] > (pix[0] + 0.2)):
                board[x,y] = OhHiGame.BLUE
            else:
                board[x,y] = OhHiGame.NONE

    game = OhHiGame.Solver(size, board)

    game.Solve()

    board_diff = game.board - board

    for point in np.argwhere(board_diff != 0):
        for n in range(board_diff[point[0],point[1]]):
            tn.write(("tap %d %d\n" % (x_axis[point[1]],y_axis[point[0]])).encode())

    if(not playForever):
        gamesToPlay = gamesToPlay - 1
    
    gamesPlayed = gamesPlayed + 1

    if(gamesPlayed % 50 == 0):
        #os.system("notify-send \"OhHi Solver\" \"Completed %d games! %d to go!\"" % (gamesPlayed, gamesToPlay))
        print("Completed $d games! %d to go!" % (gamesPlayed, gamesToPlay))

    time.sleep(4.5)

#os.system("notify-send \"OhHi Solver\" \"All Done\nCompleted %d games\"" % gamesPlayed)

clean()


