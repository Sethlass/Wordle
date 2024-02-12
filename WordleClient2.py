import tkinter as tk
from tkinter import simpledialog, messagebox
import socket 

'''
The '__init__' is responsible for creating the main GUI window where the game will be played,
creates that global variables that will be used for tracking the guesses a player has left,
and connecting to the server
'''
class WordleClientGUI:
    def __init__(self, master):
        self.master = master # Creates tkinter main window CR SL
        self.master.title("Wordle Game") # Title of the window
        self.master.configure(bg='black')  # Sets the background color of the main window

        self.connection_established = False # Checks the connection to the server
        self.max_attempts = 6 # Maximum number of attempts
        self.attempts = 0 # Number of attempts taken

        self.board_frame = tk.Frame(master, bg='black') # Frame to hold the tiles
        self.board_frame.pack(pady=(100, 0))  # Adjust padding to center

        self.tiles = [[self.create_tile(row, col) for col in range(5)] for row in range(6)] # Creates a grid layout of tiles that acts as the gameboard
        
        # Lines 24-27 deals with taking user input as a string within the GUI
        self.guess_var = tk.StringVar()
        guess_entry = tk.Entry(master, textvariable=self.guess_var, font=('Impact', 18), width=10)
        guess_entry.bind('<Return>', self.send_guess)
        guess_entry.pack(pady=20)

        wordle_label = tk.Label(master, text="WORDLE", font=('Impact', 24), fg='green', bg='black') # Creates 'WORDLE' label
        wordle_label.pack(pady=(0, 20))

        self.connect_to_server() # Establishes a connection to the server

    '''
    The 'create_tile' method is responsible for creating the design of the tiles that will be used to build the game board
    The label is the default text that the game it played with
    '''
    def create_tile(self, row, col):
        frame = tk.Frame(self.board_frame, width=60, height=60, highlightbackground='black', highlightthickness=1)
        frame.grid(row=row, column=col, padx=5, pady=5)
        label = tk.Label(frame, text="", bg='lightgray', fg='black', font=('Helvetica', 18, 'bold'))
        label.pack(expand=True, fill='both')
        return label

    '''
    The 'send_guess' method is responsible for sending the client guess to the server,
    handling the feedback messages received from the server,
    and checking if the requirements for the game to end are met
    '''
    def send_guess(self, event=None):
        if not self.connection_established: # Checks for a connection
            messagebox.showerror("Error", "Not connected to the server.")
            return
        
        guess = self.guess_var.get().upper() # Converts guess to upper case so the server can edit the feeback string
        if len(guess) != 5 or not guess.isalpha(): # If the guess is not 5-letters or is not a number
            messagebox.showerror("Error", "Invalid guess. Please enter a 5 letter word.")
            return

        self.s.sendall((guess + "\n").encode()) # Encodes the guess and sends it to the server
        feedback = self.s.recv(1024).decode().strip() # Receives the feedback response from the server
        self.process_feedback(guess, feedback) # Processes the feedback
        self.guess_var.set("") # Resets the guess string to default

        if feedback == "GGGGG" or self.attempts >= self.max_attempts: # A string of 'GGGGG' signifies that every letter is in the correct spot
            self.end_game(feedback == "GGGGG") # Ends the game

    '''
    The 'process_feedback' is responsible for analysising the feedback based on what the server returns
    '''
    def process_feedback(self, guess, feedback):
        colors = {'G': 'green', 'Y': 'yellow', 'X': 'gray'} # Map that contains a character that corresponds to the correctness of the letter 
        for i, char in enumerate(feedback): # Iterates through the feedback from the server
            tile = self.tiles[self.attempts][i] # Tile associated with 'feedback[i]'
            tile.config(text=guess[i], bg=colors[char]) # Changes the color of the tile according to the response from the server
        self.attempts += 1 # Increase the number of attempts taken

    '''
    The 'connect_to_server' method is responsible for establishing a connection to a server
    '''
    def connect_to_server(self):
        server_ip = simpledialog.askstring("Server IP", "Enter the server IP address") # Creates a popup window that asks you to enter the IP address of the server you want to connect to
        if not server_ip: # If not a valid IP address
            messagebox.showerror("Error", "No server IP entered. Exiting application.")
            self.master.quit()
            return

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((server_ip, 1234))  # Connects using the provided IP
            self.connection_established = True # Has an established connection
        except ConnectionRefusedError: # If the connection failed, output an error message and quit the server
            messagebox.showerror("Connection Error", "Could not connect to the server.")
            self.master.quit()

    '''
    The 'end_game' method is responsible for ending the game if the conditions are met
    '''
    def end_game(self, won):
        result_message = "Congratulations, you've won!" if won else "Sorry, you've lost." # Sets variable 'result_message' to "Congratulations, you've won!" if the player wins, else set it to "Sorry, you've lost" 
        messagebox.showinfo("Game Over", result_message) # Creates a popup displaying 'result_message'
        self.s.close() # Closes the socket
        self.master.quit() # Quits the server 

def main():
    root = tk.Tk() # Main instance of Tkinter
    gui = WordleClientGUI(root) # Instance of the GUI by Seth Lassiter
    root.mainloop()

if __name__ == "__main__":
    main()
