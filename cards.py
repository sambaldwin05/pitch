import os
import sys

from Tkinter import *
import tkMessageBox as tk_msg_box

class Card:
    
    SUIT_OPTIONS = {
        'c':'clubs',
        'd':'diamonds',
        'h':'hearts',
        's':'spades'
    }

    VALUE_OPTIONS = {
        2:'two',
        3:'three',
        4:'four',
        5:'five',
        6:'six',
        7:'seven',
        8:'eight',
        9:'nine',
        10:'ten',
        11:'jack',
        12:'queen',
        13:'king',
        14:'ace'
    }

    # Canvas on which we'll be drawing these cards
    CANVAS = None

    # Path to the images we'll be using.
    IMG_PATH = None

    # constructor
    def __init__(self, suit, value):
        
        # the suit and value of the card
        self.suit = suit
        self.value = value

        # the reference to the image, used by the shape
        self.photo_image = None

        # reference to the shape we draw on the canvas
        self.image_shape = None

    def draw(self, coords):
        
        # coords should be passed in as a tuple
        x, y = coords

        # create the filename
        img_filename = self.suit + str(self.value) + '.gif'

        # create the gif image
        self.photo_image = PhotoImage(
            file=os.path.join(Card.IMG_PATH, img_filename))

        self.image_shape = Card.CANVAS.create_image(
            x, y, anchor=NW, image=self.photo_image)











