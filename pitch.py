'''

NEXT STEPS

Build logic for bidding.

Build logic for assigning the winner of the trick.

'''


import os
import sys

from Tkinter import *

from gui import *
from cards import *


# Application init section.

# App display settings.
canvas_width = 800
canvas_height = 600

commands_width = 120
commands_height = canvas_height

ButtonFrame.width = commands_width
ButtonFrame.height = commands_height

# Create the tkinter window object.
top = Tk()

# Give the buttonframe class a reference to the window
# this is used in screen updates.
ButtonFrame.TK_ROOT = top

# Disable resizing.
top.resizable(width=False, height=False)

# Create the container frame to hold all the widgets.
container = Frame(top, width=(canvas_width + commands_width), 
                  height=canvas_height, bg='#444444')

# Make the container a fixed size and display it.
container.pack_propagate(0)
container.pack()

# Create the canvas.
canvas = Canvas(container, width=canvas_width, height=canvas_height, 
                bg='#00aa03', bd=0, highlightthickness=0)

status_text = StringVar()
status_text.set('This is the status bar.')

# Draw the canvas.
canvas.pack(side=LEFT)

# Set up the status bar.
status_bar = Message(top, textvariable=status_text, 
                     width=canvas_width + commands_width, anchor=W)

status_bar.pack(side=LEFT)

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

# Assign the container to be the parent widget of all the button frames.
ButtonFrame.PARENT_WIDGET = container

# Set our class level variables.
Card.CANVAS = canvas
GameState.STATUS_TEXT = status_text
Card.IMG_PATH = os.path.abspath('images/')

# Initialize some game state - or should that be done 
# with the first click of the deal button?
game_state = GameState(canvas_width, canvas_height)

# Set up the top level buttons frame on the right.
commands_frame = ButtonFrame('PITCH')

commands_frame.add_button('Deal', deal)
commands_frame.add_button('Quit', quit_app)

# Draw the main frame.
commands_frame.show()

bid_frame = ButtonFrame('Bid Amount')
bid_frame.add_button('Bid 2', lambda: game_state.set_player_bid(game_state.bid_position, 2))
bid_frame.add_button('Bid 3', lambda: game_state.set_player_bid(game_state.bid_position, 3))
bid_frame.add_button('Bid 4', lambda: game_state.set_player_bid(game_state.bid_position, 4))
bid_frame.add_button('Pass ', lambda: game_state.set_player_bid(game_state.bid_position, None))

# END BUTTONS SECTION

GameState.COMMANDS_FRAME = commands_frame
GameState.BID_FRAME = bid_frame

top.mainloop()
