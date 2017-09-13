from graphics import *
def graph(lst):
    xSpot = []
    win = GraphWin(width = 320, height = 240)
    win.setCoords(-10,-10,10,10)

    for y in range(len(lst)):
        if lst[y] == 'x':
            xSpot.append(y)
    for x in range(-1000, 1000, 1):
        for z in xSpot:
            lst[z] = x/1000

                    

