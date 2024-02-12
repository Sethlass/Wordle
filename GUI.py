import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
from colorama import init, Fore, Style

# Initialize Colorama
init()

class WordleClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Game")
        self.root.configure(bg='black')  # Set the background color to black

        # Prompt for server IP
        self.server_ip = simpledialog.askstring("Server IP", "Enter the server IP address")
        if not self.server_ip:
            messagebox.showerror("Error", "No server IP entered. Exiting application.")
            self.root.quit()
            return

        self.server_port = 1234
        self.max_attempts = 6
        self.attempts = 0
        self.connect_to_server()

        # Frame to hold the tiles (for centering purposes)
        self.board_frame = tk.Frame(root, bg='black')
        self.board_frame.pack(pady=(100, 0))  # Adjust padding as needed

        # Create the board
        self.tiles = [[self.create_tile(row, col) for col in range(5)] for row in range(6)]

        # Create input for guesses
        self.guess_var = tk.StringVar()
        guess_entry = tk.Entry(root, textvariable=self.guess_var, font=('Impact', 18), bd=3, justify='center')
        guess_entry.bind('<Return>', self.make_guess)
        guess_entry.pack(pady=20)

        # Create a label for "WORDLE"
        wordle_label = tk.Label(root, text="WORDLE", font=('Impact', 24, 'bold'), fg='green', bg='black')
        wordle_label.pack(pady=20)

    def create_tile(self, row, col):
        frame = tk.Frame(self.board_frame, width=60, height=60, bg='lightgrey', highlightbackground='black', highlightthickness=2)
        frame.grid(row=row, column=col, padx=5, pady=5)
        frame.pack_propagate(False)
        label = tk.Label(frame, text="", bg='lightgrey', fg='black', font=('Helvetica', 18, 'bold'))
        label.pack(expand=True)
        return label

    def make_guess(self, event=None):
        guess = self.guess_var.get().upper()
        if len(guess) != 5 or not guess.isalpha():
            messagebox.showerror("Error", "Invalid guess. Please enter a 5 letter word.")
            self.guess_var.set("")
            return

        # Send guess to the server and receive feedback
        self.s.sendall((guess.lower() + "\n").encode())
        feedback = self.s.recv(1024).decode().strip()

        # Display feedback
        self.display_feedback(guess, feedback)
        self.guess_var.set("")

        # Check for game end
        self.attempts += 1
        if feedback == "GGGGG" or self.attempts >= self.max_attempts:
            self.end_game(feedback == "GGGGG")

    def display_feedback(self, guess, feedback):
        for i, tile in enumerate(self.tiles[self.attempts]):
            tile['text'] = guess[i]
            if feedback[i] == 'G':
                tile['bg'] = 'green'
            elif feedback[i] == 'Y':
                tile['bg'] = 'yellow' #CR SL
            else:
                tile['bg'] = 'grey'

    def connect_to_server(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.server_ip, self.server_port))
            print("Connected to the server.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to the server: {e}")
            self.root.quit()

    def end_game(self, won):
        message = "Congratulations! You guessed the word!" if won else "Game Over! You've reached the maximum number of attempts."
        messagebox.showinfo("Game Over", message)
        self.s.close()  # Close the socket
        self.root.quit()  # Close the application

# Create the main window
root = tk.Tk()
app = WordleClientGUI(root)

# Run the application CR: SL
root.mainloop()




















#Created by Seth Lassiter
