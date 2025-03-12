import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from random import shuffle, choice

# Constants
CUSTOM_FONT_PATH = "OpenSans-Regular.ttf"  # Path to your uploaded font

class DominoesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dominoes Game")
        self.root.configure(bg="saddlebrown")

        # Initialize game variables
        self.tiles = [(i, j) for i in range(7) for j in range(i, 7)]
        shuffle(self.tiles)  # Shuffle tiles randomly
        self.player_tiles = []
        self.computer_tiles = []
        self.chain = []  # Initially empty, will be set in the first round
        self.remaining_tiles = self.tiles[:]  # Remaining tiles for drawing
        self.player_score = 0
        self.computer_score = 0
        self.selected_tile = None
        self.round_first_player = None

        # GUI Elements
        self.create_gui()
        self.start_new_round()

    def create_gui(self):
        
        # Chain Display
        self.chain_frame = tk.Frame(self.root, bg="darkgoldenrod")
        self.chain_frame.pack(pady=10, fill="x")
        self.chain_tiles_frame = tk.Frame(self.chain_frame, bg="darkgoldenrod")
        self.chain_tiles_frame.pack(anchor="center")

        # Player Tiles
        self.tiles_frame = tk.Frame(self.root, bg="darkgoldenrod", padx=10, pady=10)
        self.tiles_frame.pack(pady=10)
        self.update_player_tiles()

        # Action Buttons
        self.actions_frame = tk.Frame(self.root, bg="darkgoldenrod")
        self.actions_frame.pack(pady=60)
        self.left_button = tk.Button(
            self.actions_frame,
            text="Left",
            font=("Open Sans", 20),
            command=lambda: self.play_tile("left"),
            bg="sienna",
            fg="white",
            padx=30,
        )
        self.left_button.grid(row=0, column=0, padx=10)

        self.right_button = tk.Button(
            self.actions_frame,
            text="Right",
            font=("Open Sans", 20),
            command=lambda: self.play_tile("right"),
            bg="olive",
            fg="white",
            padx=30,
        )
        self.right_button.grid(row=0, column=1, padx=10)

        # Scoring Display
        self.info_frame = tk.Frame(self.root, bg="saddlebrown")
        self.info_frame.pack(pady=20)

        self.player_score_label = tk.Label(
            self.info_frame, text=f"Player Score: {self.player_score}", font=("Open Sans", 20, "bold"), bg="lightpink", fg="black"
        )
        self.player_score_label.grid(row=0, column=0, padx=20)

        self.computer_score_label = tk.Label(
            self.info_frame, text=f"Computer Score: {self.computer_score}", font=("Open Sans", 20, "bold"), bg="lightblue", fg="black"
        )
        self.computer_score_label.grid(row=0, column=1, padx=20)

        self.computer_tiles_label = tk.Label(
            self.info_frame, text=f"Computer Tiles: 0", font=("Open Sans", 20, "bold"), bg="lightgreen", fg="black"
        )
        self.computer_tiles_label.grid(row=1, column=0, padx=20)

        self.remaining_tiles_label = tk.Label(
            self.info_frame, text=f"Remaining Tiles: {len(self.remaining_tiles)}", font=("Open Sans", 20, "bold"), bg="lightyellow", fg="black"
        )
        self.remaining_tiles_label.grid(row=1, column=1, padx=20)
        self.chain_canvas = tk.Canvas(self.chain_frame, bg="darkgoldenrod")
        self.chain_scrollbar = ttk.Scrollbar(
        self.chain_frame, orient="horizontal", command=self.chain_canvas.xview   
     )
        self.chain_tiles_frame = tk.Frame(self.chain_canvas, bg="darkgoldenrod")

        self.chain_tiles_window = self.chain_canvas.create_window(
        (0, 0), window=self.chain_tiles_frame, anchor="nw"
         )
        self.chain_canvas.config(xscrollcommand=self.chain_scrollbar.set)

        self.chain_canvas.pack(side="top", fill="both", expand=True)
        self.chain_scrollbar.pack(side="bottom", fill="x")
        # Update the initial chain display
        self.update_chain_display()

    def start_new_round(self):
        # Reset variables for the new round
        self.chain = []
        self.remaining_tiles = [(i, j) for i in range(7) for j in range(i, 7)]
        shuffle(self.remaining_tiles)
        self.player_tiles = [self.remaining_tiles.pop() for _ in range(7)]
        self.computer_tiles = [self.remaining_tiles.pop() for _ in range(7)]
        self.selected_tile = None

        if hasattr(self, "last_winner"):  # Check if there's a previous round winner
            if self.last_winner == "player":
                self.round_first_player = "player"
                messagebox.showinfo("New Round", "You won the last round. You start this round!")
                self.play_tile("left") or self.play_tile("right")  # Start the player's turn
            elif self.last_winner == "computer":
                self.round_first_player = "computer"
                messagebox.showinfo("New Round", "The computer won the last round. It starts this round!")
                self.computer_turn()  # Start the computer's turn
        else:
            # First round logic: determine the first player based on the largest symmetric tuple
            largest_symmetric_player = max([tile for tile in self.player_tiles if tile[0] == tile[1]], default=None)
            largest_symmetric_computer = max([tile for tile in self.computer_tiles if tile[0] == tile[1]], default=None)

            if largest_symmetric_player and (not largest_symmetric_computer or largest_symmetric_player > largest_symmetric_computer):
                self.round_first_player = "player"
                self.player_tiles.remove(largest_symmetric_player)
                self.chain.append(largest_symmetric_player)
                messagebox.showinfo("First Move", f"You start with {largest_symmetric_player}.")
                self.update_chain_display()  # Update the chain display
                self.update_player_tiles()
                self.update_info()
                self.computer_turn()  # Pass the turn to the computer
            elif largest_symmetric_computer:
                self.round_first_player = "computer"
                self.computer_tiles.remove(largest_symmetric_computer)
                self.chain.append(largest_symmetric_computer)
                messagebox.showinfo("First Move", f"Computer starts with {largest_symmetric_computer}.")
                self.update_chain_display()  # Update the chain display
                self.update_player_tiles()
                self.update_info()
            else:
                # No symmetric tiles, player starts
                self.round_first_player = "player"
                messagebox.showinfo("Game Start", "No symmetric tiles found. You start the game!")

        # Update all GUI displays
        self.update_chain_display()  # Make sure the chain is updated
        self.update_player_tiles()   # Update player tiles display
        self.update_info()           # Update any other information (e.g., scores)





    def update_player_tiles(self):
        for widget in self.tiles_frame.winfo_children():
            widget.destroy()
        tile_count = len(self.player_tiles)
        tile_size = max(80, 200 - tile_count * 10)  # Decrease size as the number of tiles increases
        
        for tile in self.player_tiles:
            btn = tk.Button(
                self.tiles_frame,
                text=str(tile),
                font=("Open Sans", 20),
                command=lambda t=tile: self.select_tile(t),
                bg="white",
                fg="black",
                padx=30,
                pady=20,
                borderwidth=4,
                relief="solid",
            )
            btn.pack(side="left", padx=10)

    def update_chain_display(self):
     # Clear the current chain display
        for widget in self.chain_tiles_frame.winfo_children():
            widget.destroy()

     # Set a fixed tile size
        tile_size = 100  # Fixed tile size (you can adjust this value)

        # Arrange tiles dynamically
        for tile in self.chain:
            lbl = tk.Label(
                self.chain_tiles_frame,
                text=str(tile),
                font=("Open Sans", max(10, int(tile_size * 0.25))),  # Adjust font size
                bg="white",
                fg="black",
                width=int(tile_size / 20),
                height=int(tile_size / 40),
                borderwidth=4,
                relief="solid",
            )
            lbl.pack(side="left", padx=5)

        # Dynamically adjust the frame height
        self.chain_tiles_frame.config(height=tile_size + 20)



    def update_scores_display(self):
        self.player_score_label.config(text=f"Player Score: {self.player_score}")
        self.computer_score_label.config(text=f"Computer Score: {self.computer_score}")

    def update_info(self):
        self.computer_tiles_label.config(text=f"Computer Tiles: {len(self.computer_tiles)}")
        self.remaining_tiles_label.config(text=f"Remaining Tiles: {len(self.remaining_tiles)}")

    def select_tile(self, tile):
        self.selected_tile = tile
        messagebox.showinfo("Tile Selected", f"You selected {tile}.")

    def play_tile(self, side):
    # Check if the player has any valid moves
        if not any(self.is_match_side(tile, "left") or self.is_match_side(tile, "right") for tile in self.player_tiles):
            messagebox.showinfo("No Valid Moves", "No valid moves. Drawing tiles automatically.")
        
            # Keep drawing tiles until a valid one is found or tiles run out
            while self.draw_tile(player="player"):
                if any(self.is_match_side(tile, "left") or self.is_match_side(tile, "right") for tile in self.player_tiles):
                    self.update_player_tiles()  # Refresh player tiles
                    return  # Exit the function; player can now make a valid move

            # If no valid tile found after drawing, check for blocked round
            if self.check_blocked():
                return self.end_round(winner="blocked")
            else:
                messagebox.showinfo("Turn Passed", "No valid tiles. Passing turn to the computer.")
                return self.computer_turn()

        # If the player has selected a tile and it's valid, proceed to play it
        elif hasattr(self, "selected_tile") and self.selected_tile in self.player_tiles:
            if self.is_match_side(self.selected_tile, side):
                self.player_tiles.remove(self.selected_tile)
                self.place_tile_side(self.selected_tile, side)
                self.selected_tile = None
                self.update_player_tiles()
                self.update_chain_display()

                if not self.player_tiles:
                    self.end_round(winner="player")
                else:
                    self.computer_turn()
            else:
                messagebox.showerror("Invalid Move", f"Tile doesn't match on the {side}!")

        else:
            messagebox.showerror("No Tile Selected", "Select a tile first!")

    
    def check_blocked(self):
        # Check if neither the player nor computer has valid moves
        player_valid = any(
            self.is_match_side(tile, ",left") or self.is_match_side(tile, "right")
            for tile in self.player_tiles
        )
        computer_valid = any(
            self.is_match_side(tile, "left") or self.is_match_side(tile, "right")
            for tile in self.computer_tiles
        )
        return not player_valid and not computer_valid and not self.remaining_tiles


    def is_match_side(self, tile, side):
        if side == "left":
            return tile[0] == self.chain[0][0] or tile[1] == self.chain[0][0]
        elif side == "right":
            return tile[0] == self.chain[-1][1] or tile[1] == self.chain[-1][1]

    def place_tile_side(self, tile, side):
        if side == "left":
            if tile[1] == self.chain[0][0]:
                self.chain.insert(0, tile)
            else:
                self.chain.insert(0, (tile[1], tile[0]))
        elif side == "right":
            if tile[0] == self.chain[-1][1]:
                self.chain.append(tile)
            else:
                self.chain.append((tile[1], tile[0]))

    def draw_tile(self, player):
        while self.remaining_tiles:
        # Draw a tile from the remaining tiles
            new_tile = self.remaining_tiles.pop(0)
            if player == "player":
               self.player_tiles.append(new_tile)
               self.update_info()  # Update info to reflect the draw
            
            # Check if the drawn tile is valid
               if self.is_match_side(new_tile, "left") or self.is_match_side(new_tile, "right"):
                # If valid, play it automatically
                  self.player_tiles.remove(new_tile)
                  self.place_tile_side(new_tile, "left" if self.is_match_side(new_tile, "left") else "right")
                  self.update_chain_display()
                  return True  # Player turn ends after playing a valid tile
            elif player == "computer":
                self.computer_tiles.append(new_tile)
                self.update_info()  # Update info to reflect the draw
            
            # Check if the drawn tile is valid
                if self.is_match_side(new_tile, "left") or self.is_match_side(new_tile, "right"):
                # If valid, play it automatically
                   self.computer_tiles.remove(new_tile)
                   self.place_tile_side(new_tile, "left" if self.is_match_side(new_tile, "left") else "right")
                   self.update_chain_display()
                   return True  # Computer turn ends after playing a valid tile

    # If no tiles are left to draw, return False
        return False




    def computer_turn(self):
     available_moves = [
        (tile, side)
        for tile in self.computer_tiles
        for side in ["left", "right"]
        if self.is_match_side(tile, side)
     ]

     if available_moves:
        # Play one tile only
        tile, side = choice(available_moves)
        self.computer_tiles.remove(tile)
        self.place_tile_side(tile, side)
        self.update_chain_display()
        self.update_info()
     else:
        # No valid move; try drawing tiles until a valid one is found
        if not self.draw_tile(player="computer"):
            # If drawing fails (no remaining tiles), pass the turn
            messagebox.showinfo("Turn Passed", "No valid moves for computer. Your turn.")

     self.update_info()

     if not self.computer_tiles:
        self.end_round(winner="computer")
    #  elif not any(self.is_match_side(tile, "ledt") or self.is_match_side(tile, "end") for tile in self.player_tiles):
    #     # Pass turn back to the player if no valid moves
    #     self.computer_turn()
     else:
         self.update_info()

    def calculate_score(self, winner):
        """
        Calculate the score based on the end-game scenario.
        """
        # Sum up the values of the remaining tiles for each player
        player_tile_sum = sum(sum(tile) for tile in self.player_tiles)
        computer_tile_sum = sum(sum(tile) for tile in self.computer_tiles)

        if winner == "player":
            self.player_score += computer_tile_sum
            messagebox.showinfo("Round Over", f"You won this round! You gain {computer_tile_sum} points.")
        elif winner == "computer":
            self.computer_score += player_tile_sum
            messagebox.showinfo("Round Over", f"Computer won this round! It gains {player_tile_sum} points.")
        elif winner == "draw":
            messagebox.showinfo("Round Over", "It's a draw! No points awarded.")

        # Update the scores in the UI
        self.update_scores_display()

        # Check if the game should end
        if self.player_score >= 101 or self.computer_score >= 101:
            if self.player_score > self.computer_score:
                messagebox.showinfo("Game Over", f"Congratulations! You won the game with {self.player_score} points!")
            else:
                messagebox.showinfo("Game Over", f"Computer wins the game with {self.computer_score} points! Better luck next time.")
            self.reset_game()
        else:
            self.start_new_round()

    def end_round(self, winner):
        """
        Handles the end of a round.
        """
        if winner == "player":
            self.calculate_score("player")
        elif winner == "computer":
            self.calculate_score("computer")
        elif winner == "blocked":
            # Compare the sums of remaining tiles
            player_tile_sum = sum(sum(tile) for tile in self.player_tiles)
            computer_tile_sum = sum(sum(tile) for tile in self.computer_tiles)

            if player_tile_sum < computer_tile_sum:
                self.calculate_score("player")
            elif computer_tile_sum < player_tile_sum:
                self.calculate_score("computer")
            else:
                self.calculate_score("draw")



root = tk.Tk()
app = DominoesApp(root)
root.mainloop()