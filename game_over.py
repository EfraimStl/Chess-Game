from tkinter import *
from main import main

FONT = ("Arial", 70, "bold")

class GameOver:
    def __init__(self, color):
        self.color = color
        self.window = Tk()
        self.window.title("Game Over")
        self.window.configure(bg="#D5EEBB", padx=20, pady=20)

        # Get the screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        window_width = (screen_width - self.window.winfo_reqwidth())

        # Set the window size to match the screen size
        self.window.geometry(f"700x700+{window_width // 4}+{0}")

        self.game_over_label = Label(text=f"Game Over", foreground="#5F7A61", background="#D5EEBB", font=("Arial", 50, "bold"))
        self.game_over_label.grid(column=0, row=0, pady=30)
        self.who_wins_label = Label(text=f"{self.color}",  foreground=self.color, background="#D5EEBB", font=FONT)
        self.who_wins_label.grid(column=0, row=1, pady=15)
        self.player_win_label = Label(text="player win", foreground="#5F7A61", background="#D5EEBB", font=FONT)
        self.player_win_label.grid(column=0, row=2, padx=80)
        self.button = Button(text="Play Again", background="#5F7A61", command=self.start_again, font=("Arial", 30, "bold"), bd=5)
        self.button.grid(column=0, row=3, pady=60)

        self.window.mainloop()

    def start_again(self):
        self.window.destroy()
        main()

