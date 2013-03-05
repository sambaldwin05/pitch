import os
import sys
import random

from Tkinter import *

from gui import *
from cards import *


# application init section

# app display settings
canvas_width = 800
canvas_height = 600

commands_width = 120
commands_height = canvas_height

ButtonFrame.width = commands_width
ButtonFrame.height = commands_height

# create the tkinter window object
top = Tk()

# give the buttonframe class a reference to the window
# this is used in screen updates
ButtonFrame.TK_ROOT = top

# disable resizing
top.resizable(width=False, height=False)

# create the container frame to hold all the widgets
container = Frame(top, width=(canvas_width + commands_width), 
                        height=canvas_height, bg='#444444')

# make the container a fixed size and display it
container.pack_propagate(0)
container.pack()

# create the canvas
canvas = Canvas(container, width=canvas_width, height=canvas_height, 
                            bg='#00aa03', bd=0, highlightthickness=0)

status_text = StringVar()
status_text.set('This is the status bar.')

# draw the canvas
canvas.pack(side=LEFT)

# set up the status bar
status_bar = Message(top, textvariable=status_text, 
                        width=canvas_width + commands_width, anchor=W)

status_bar.pack(side=LEFT)

# BUTTONS SECTION

# build out helper functions
def quit_app():
    print 'You have quit pitch.  Quitter.'
    sys.exit(0)

# gotta keep a reference - this will become
# part of the deck class (probably)
deck = []

def deal():

    # build a deck
    for suit in Card.SUIT_OPTIONS.keys():
        for value in Card.VALUE_OPTIONS.keys():
            card = Card(suit, value)
            deck.append(card)
    
    random.shuffle(deck)

    # draw each card in a random space
    i = 1
    for card in deck:
        card.draw((random.randint(0, canvas_width - 80), 
            random.randint(0, canvas_height - 100)))
        print '%d: %s of %s' % (i, Card.VALUE_OPTIONS[card.value],
            Card.SUIT_OPTIONS[card.suit])
        i += 1

    text = ('Dealing a deck of 52 cards in random order.')
    status_text.set(text)

# assign the container to be the parent widget of all the button frames
ButtonFrame.PARENT_WIDGET = container

# set up the top level buttons frame on the right
commands_frame = ButtonFrame('PITCH')

commands_frame.add_button('Deal', deal)
commands_frame.add_button('Quit', quit_app)

# draw the main frame
commands_frame.show()

# END BUTTONS SECTION

# Set our class level variables
Card.CANVAS = canvas
Card.IMG_PATH = os.path.abspath('images/')

# initialize some game state - maybe?
# should that be done with the first click of the deal button?

top.mainloop()


