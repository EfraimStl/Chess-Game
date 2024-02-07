import board_gui
import game_logic


def main():
    """
    Main function to run the game
    """
    logic = game_logic.GameLogic()
    gui = board_gui.BoardGui(logic)
    gui.root.mainloop()


if __name__ == '__main__':
    main()
