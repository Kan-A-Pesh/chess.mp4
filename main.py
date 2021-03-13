import board, render, sys, game

grid = board.Plateau()
selected = -1
available = []

def onClick(pos):
    global grid, available, selected
    if (selected == -1 and not grid.isEmpty(pos)):
        selected = pos
        
        render.addHighlight(pos, 0)
        for i in game.getMoves(grid, selected):
            if (grid.isEmpty(i)):
                render.addHighlight(i, 1)
            else:
                render.addHighlight(i, 2)
            available.append(i)
    else:
        if (available.__contains__(pos)):
            grid.move(selected, pos)

        selected = -1
        available = []
        render.removeHighlights()
    render.render(grid)

if __name__ == "__main__":
    render.init()
    render.registerCallback("onClick", onClick)
    render.render(grid)
    while 1:
        if render._isAlive == False: sys.exit()