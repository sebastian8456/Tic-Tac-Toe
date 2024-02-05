# Game.py
# Starts the TicTacToe game
# TODO: Refactor by moving the classes methods into functions and running the game through main.py
import tkinter as tk
import random
import copy
import time
from tkinter import font

FONT = ("Ariel", 32)

class Game:
    def __init__(self):
        self.player_count = 0
        self.playing = True
        
        # Create the game board
        self.board = [[" " for j in range(3)] for i in range(3)]
        self.buttons = [[None for j in range(3)] for i in range(3)]

        # Create the root window
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(width=False, height=False)
        self.root.geometry("448x815+600+100")   
        self.root.withdraw()

        # Create the main frame for the game
        self.content = tk.Frame(self.root)
        self.content.grid(sticky="NSEW", padx=10)
        self.configure_frame(self.content, 1, 5, 4)
        
        # Create and modify the starting screen
        self.start_screen = tk.Toplevel()
        self.start_screen.title("Tic-Tac-Toe")
        self.start_screen.geometry("265x215+600+100")
        self.start_screen.attributes('-topmost',True)
        self.start_screen.resizable(width=False, height=False)
        
        self.start_screen_content = tk.Frame(self.start_screen)
        self.start_screen_content.grid(sticky="NSEW", padx=10)
        self.configure_frame(self.start_screen_content, 1, 3, 2)
        
        self.start_screen_header = tk.Label(self.start_screen_content, text="Tic-Tac-Toe", font=FONT)
        self.start_screen_header.grid(column=0, row=0, columnspan=2)
        
        self.one_player_button = tk.Button(self.start_screen_content, command=self.one_player_clicked, text="1 Player", bg="white", font=("Ariel", 18), height=1, width=10)
        self.one_player_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.one_player_button = tk.Button(self.start_screen_content, command=self.two_player_clicked, text="2 Player", bg="white", font=("Ariel", 18), height=1, width=10)
        self.one_player_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        
        # Create a Tic-Tac-Toe header
        self.header = tk.Label(self.content, text="Tic-Tac-Toe", font=FONT)
        self.header.grid(row=0, column=0, columnspan=4)

        # Create the display for the game
        self.text = tk.StringVar()
        self.text.set(f"{self.player(self.board)}'s Turn")
        self.display = tk.Label(self.content, textvariable=self.text, height=2, width=20, font=('Ariel', 24), bg='White', relief="ridge", bd=4)
        self.display.grid(column=0, columnspan=3, row=4, pady=10)
        
        # Display the win count
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.wins_string = tk.StringVar()
        self.wins_string.set(f"X wins: {self.x_wins}\nO wins: {self.o_wins}\nDraws: {self.draws}")
        self.wins_display = tk.Label(self.content, textvariable=self.wins_string, justify=tk.LEFT, font=("Ariel", 16), height=3, width=8)
        self.wins_display.grid(column=0, row=5, rowspan=2)
                                       
        # Reset button
        self.reset_button = tk.Button(self.content, font=("Ariel", 18), command=self.reset_game, text="Reset", height=2, width=10, relief='groove')
        self.reset_button.grid(column=1, row=5, rowspan=2)
    
        # Generate a 3x3 grid
        self.grid_generator(3, 3, 3)
        
        # Initialize button commands
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].configure(command=lambda col=col, row=row: self.on_click(row, col))
        
        self.root.mainloop()

    def one_player_clicked(self):
        self.player_count = 1
        self.start_game()
    
    def two_player_clicked(self):
        self.player_count = 2
        self.start_game()
        
    def start_game(self):
        self.start_screen.withdraw()
        self.root.deiconify()
    

    def grid_generator(self, size, columns, rows):
        # Generate buttons for the tic-tac-toe grid
        for col in range(columns):
            for row in range(rows):
                button = tk.Button(self.content, bg='#aaaaaa', text="", font=FONT, width=size+2, height=size)
                button.grid(column=col, row=row+1, sticky="NSEW", padx=2, pady=2)
                self.buttons[row][col] = button
                
    def configure_frame(self, frame, weight, rows, columns):
        # Style the main frame's structure
        for i in range(rows):
            frame.rowconfigure(i, weight=weight)
        for i in range(columns):
            frame.columnconfigure(i, weight=weight)
            
    def reset_game(self):
        # Clear shapes from the board and buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text="", state="normal")
                self.board[i][j] = " "
        self.text.set(f"{self.player(self.board)}'s Turn")
        self.playing = True

    def disable_buttons(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].configure(state="disabled")

    def check_board(self):
        if self.winner(self.board) != None:
            self.text.set(f'{self.winner(self.board)} wins!')
            # The player will be reversed since the turn changed
            if self.player(self.board) == 'O':
                self.x_wins += 1
            else:
                self.o_wins += 1
        elif self.terminal(self.board):
            self.text.set("Draw!")
            self.draws += 1
        else:
            return
        self.playing = False
        self.disable_buttons()

    def on_click(self, row, col):
        # Update the button's shape(X/O) upon being clicked
        if self.space_check(row, col):
            self.buttons[row][col].configure(text=self.player(self.board))
            self.board[row][col] = self.player(self.board)
        else:
            return
        self.check_board()
        if self.playing and self.player_count == 1:
            self.text.set("Computer thinking...")
            self.display.update()
            # AI player's turn
            pos1, pos2 = self.minimax(self.board)
            self.buttons[pos1][pos2].configure(text=self.player(self.board))
            self.board[pos1][pos2] = self.player(self.board)
    
            self.check_board()

        if self.playing:
            self.text.set(f"{self.player(self.board)}'s Turn")

        # Update wins string
        self.wins_string.set(f"X wins: {self.x_wins}\nO wins: {self.o_wins}\nDraws: {self.draws}")

    def terminal(self, board):
        if self.winner(board) != None:
            return True
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    return False
        return True

    def space_check(self, row, col):
        return self.board[row][col] == " "
    

    def winner(self, board):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != " ":
                return board[i][0]
            elif board[0][i] == board[1][i] == board[2][i] != " ":
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != " " or board[2][0] == board[1][1] == board[0][2] != " ":
                return board[1][1]
        return None

    def actions(self, board):
        """Returns set of (i, j) actions for a board."""
        actions = set()
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    actions.add((i, j))
        return actions


    def player(self, board):
        counter = 0
        for row in board:
            for cell in row:
                if cell != " ":
                    counter += 1
        if counter % 2 == 0:
            return "X"
        else:
            return "O"

    def result(self, board, action):
        new_board = copy.deepcopy(board)
        row, cell = action
        if new_board[row][cell] == " ":
            new_board[row][cell] = self.player(board)
        else:
            raise Exception("Invalid action.")
        return new_board

    def utility(self, board):
        if self.winner(board) == "X":
            return 1
        elif self.winner(board) == "O":
            return -1
        else:
            return 0

    def min_value(self, board):
        if self.terminal(board):
            return self.utility(board)
        v = 999999
        for action in self.actions(board):
            v = min(v, self.max_value(self.result(board, action)))
        return v

    def max_value(self, board):
        if self.terminal(board):
            return self.utility(board)
        v = -999999
        for action in self.actions(board):
            v = max(v, self.min_value(self.result(board, action)))
        return v

    def minimax(self, board):
        """Returns the optimal move for the player to move on the board."""
        top_action = None
        top_value = 0
        
        if self.terminal(board):
            return None
        for action in self.actions(board):
            min = self.min_value(self.result(board, action))
            max = self.max_value(self.result(board, action))
            if min >= top_value and self.player(board) == "X":
                top_action = action
                top_value = min
            elif max <= top_value and self.player(board) == "O":
                top_action = action
                top_value = max
        return top_action
