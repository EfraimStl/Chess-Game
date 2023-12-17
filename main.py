import board_gui
import game_logic

if __name__ == '__main__':
    game_logic = game_logic.GameLogic()
    board_gui = board_gui.BoardGui(game_logic)
    board_gui.root.mainloop()
