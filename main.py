def main():
    """
    Main function to run the game
    """
    import board_gui
    import game_logic
    game_logic = game_logic.GameLogic()
    board_gui = board_gui.BoardGui(game_logic)
    board_gui.root.mainloop()


if __name__ == '__main__':
    main()
