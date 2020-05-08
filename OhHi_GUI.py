import numpy as np
import wx
import sys
import OhHiGame


class OhHi_GUI(wx.Frame):

    def __init__(self, size):
        super(OhHi_GUI, self).__init__(None, title="OhHi")

        self.size = size

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.InitUI()
        self.SetSizer(self.vbox)
        self.Centre()

    def InitUI(self):
        defaultBoard = np.full([self.size, self.size], OhHiGame.NONE)
        self.game = OhHiGame.Solver(self.size, defaultBoard)

        self.AddMenuBar()

        gs = wx.GridSizer(self.size, self.size, 5, 5)

        self.ButtonList = []
        for x in range(self.size):
            for y in range(self.size):
                but = wx.Button(self, label='')
                but.Bind(wx.EVT_BUTTON, lambda event, x=x, y=y:
                         self.OnButtonClick(event, x, y))
                self.ButtonList.append(but)

        gs.AddMany([(button, 0, wx.EXPAND) for button in self.ButtonList])

        self.vbox.Add(gs, proportion=1, flag=wx.EXPAND)

    def AddMenuBar(self):
        gameMenu = wx.Menu()
        solveItem = gameMenu.Append(-1, "&Solve", "Solve the game board")
        gameMenu.AppendSeparator()
        resizeGameItem = gameMenu.Append(-1, "&New Size",
                                         "Create a game with new size")
        gameMenu.AppendSeparator()
        newGameItem = gameMenu.Append(-1, "&New Game", "Create a new game")
        gameMenu.AppendSeparator()

        menuBar = wx.MenuBar()
        menuBar.Append(gameMenu, '&Game')
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnSolve, solveItem)
        self.Bind(wx.EVT_MENU, self.OnNewGame, newGameItem)
        self.Bind(wx.EVT_MENU, self.OnResizeGame, resizeGameItem)

    def OnButtonClick(self, event, x, y):
        but = event.GetEventObject()
        board = self.game.board
        if (board[x, y] == OhHiGame.RED):
            board[x, y] = OhHiGame.BLUE
            but.SetBackgroundColour(wx.Colour(0, 0, 255))
        elif (board[x, y] == OhHiGame.NONE):
            board[x, y] = OhHiGame.RED
            but.SetBackgroundColour(wx.Colour(255, 0, 0))
        elif (board[x, y] == OhHiGame.BLUE):
            board[x, y] = OhHiGame.NONE
            but.SetBackgroundColour(wx.NullColour)

    def UpdateButtonColors(self):
        flatBoard = self.game.board.flatten()
        for i in range(flatBoard.size):
            color = flatBoard[i]
            but = self.ButtonList[i]
            if(color == OhHiGame.NONE):
                but.SetBackgroundColour(wx.NullColour)
            elif(color == OhHiGame.BLUE):
                but.SetBackgroundColour(wx.Colour(0, 0, 255))
            elif(color == OhHiGame.RED):
                but.SetBackgroundColour(wx.Colour(255, 0, 0))

    def OnSolve(self, event):
        self.game.Solve()
        self.UpdateButtonColors()

    def OnNewGame(self, event):
        self.game.board = np.full([self.size, self.size], OhHiGame.NONE)
        self.UpdateButtonColors()

    def OnResizeGame(self, event):
        dlg = wx.TextEntryDialog(None, 'Enter a size multiple of 2',
                                 'Enter Size')
        dlg.SetValue(str(self.size))
        if (dlg.ShowModal() == wx.ID_OK):
            newSize = int(dlg.GetValue())
            if(newSize % 2 == 0):
                self.vbox.Clear(True)
                self.size = newSize
                self.InitUI()

        dlg.Destroy()


def main():
    size = 4

    if(len(sys.argv) == 2):
        size = int(sys.argv[1])

    app = wx.App()
    ex = OhHi_GUI(size)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
