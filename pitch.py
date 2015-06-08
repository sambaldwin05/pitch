'''

NEXT STEPS

Build logic for bidding.

Build logic for assigning the winner of the trick.

'''


import os
import sys

import Tkinter as tk

from gui import GuiFrame, ButtonFrame, StatusFrame
from cards import Card, GameState


# Application init section.

# App display settings.
canvas_width = 800
canvas_height = 600

commands_width = 120
commands_height = 300

# Create the tkinter window object.
top = tk.Tk()

# Give the buttonframe class a reference to the window
# this is used in screen updates.
GuiFrame.TK_ROOT = top

# Disable resizing.
top.resizable(width=False, height=False)

# Create the container frame to hold all the widgets.
container = tk.Frame(top, width=(canvas_width + commands_width), 
                  height=canvas_height, bg='#444444')

# Make the container a fixed size and display it.
container.pack_propagate(0)
container.pack()

# Create the canvas.
canvas = tk.Canvas(container, width=canvas_width, height=canvas_height, 
                   bg='#00aa03', bd=0, highlightthickness=0)

status_text = tk.StringVar()
status_text.set('This is the status bar.')

# Draw the canvas.
canvas.pack(side=tk.LEFT)

# Set up the status bar.
status_bar = tk.Message(top, textvariable=status_text, 
                        width=canvas_width + commands_width, anchor=tk.W)
status_bar.pack(side=tk.LEFT)


# Assign the container to be the parent widget of all the button frames.
GuiFrame.PARENT_WIDGET = container

# Set our class level variables.
Card.CANVAS = canvas
GameState.STATUS_TEXT = status_text
Card.IMG_PATH = os.path.abspath('images/')

# Initialize our game state.
game_state = GameState(canvas_width, canvas_height)

# Set up the top level buttons frame on the right.
commands_frame = ButtonFrame('PITCH', height=commands_height)

# BUTTONS SECTION

# Build out helper functions.
def quit_app():
    print 'You have quit pitch.  Quitter.'
    sys.exit(0)

def deal():
    game_state.deal_hands(2)

    # Disable the deal button.
    commands_frame.disable_button_by_text('Deal')

    text = 'Dealing a deck of 52 cards in random order.'
    status_text.set(text)


commands_frame.add_button('Deal', deal)
commands_frame.add_button('Quit', quit_app)

# Draw the main frame.
commands_frame.show()

bid_frame = ButtonFrame('Bid Amount', height=commands_height)
bid_frame.add_button(
    'Bid 2', lambda: game_state.set_player_bid(game_state.bid_position, 2)
)
bid_frame.add_button(
    'Bid 3', lambda: game_state.set_player_bid(game_state.bid_position, 3)
)
bid_frame.add_button(
    'Bid 4', lambda: game_state.set_player_bid(game_state.bid_position, 4)
)
bid_frame.add_button(
    'Pass ', lambda: game_state.set_player_bid(game_state.bid_position, None)
)

# END BUTTONS SECTION

# Build our status frame to show the game state.
status_frame = StatusFrame(
    text='Scoreboard', width=commands_width, height=commands_height
)
status_frame.show()

GameState.COMMANDS_FRAME = commands_frame
GameState.BID_FRAME = bid_frame
GameState.STATUS_TEXT = status_text
GameState.SCORE_FRAME = status_frame

top.mainloop()
