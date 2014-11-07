import os
import sys
import random
import time

from Tkinter import *
import tkMessageBox as tk_msg_box


class Card:
    
    SUIT_OPTIONS = {
        'c': 'Clubs',
        'd': 'Diamonds',
        'h': 'Hearts',
        's': 'Spades'
    }

    VALUE_OPTIONS = {
        2: 'Two',
        3: 'Three',
        4: 'Four',
        5: 'Five',
        6: 'Six',
        7: 'Seven',
        8: 'Eight',
        9: 'Nine',
        10: 'Ten',
        11: 'Jack',
        12: 'Queen',
        13: 'King',
        14: 'Ace'
    }

    # Canvas on which we'll be drawing these cards.
    CANVAS = None

    # Text status area we'll update.
    STATUS_TEXT = None

    # Path to the images we'll be using.
    IMG_PATH = None
    BACK_IMG_FILENAME = 'b1fv.gif'

    # Constructor.
    def __init__(self, suit, value):
        
        # The suit and value of the card.
        self.suit = suit
        self.value = value

        # The reference to the image, used by the shape.
        self.photo_image = None

        # Reference to the shape we draw on the canvas.
        self.image_shape = None

        # Reference to the hand that owns this card.
        self.player_hand = None

    def game_value(self):
        game_value = self.value - 10
        if game_value == 0:
            game_value = 10
        if game_value >= 0:
            return game_value
        else:
            return 0

    def draw(self, x, y):
        # Store the coordinates of this card.
        self.coords = (x, y)
        self.face_up = True

        # Create the filename.
        img_filename = self.suit + str(self.value) + '.gif'

        # Create the gif image.
        self.photo_image = PhotoImage(
            file=os.path.join(Card.IMG_PATH, img_filename))

        self.image_shape = Card.CANVAS.create_image(
            x, y, anchor=NW, image=self.photo_image)

        # Bind an event to the click.
        Card.CANVAS.tag_bind(self.image_shape, '<Button-1>', 
                             lambda X: self._play_card())

    def undraw(self):
        self.coords = (None, None)
        self.face_up = False
        Card.CANVAS.delete(self.image_shape)
        self.image_shape = None
        self.photo_image = None

    def card_name(self):
        return '%s of %s' % (Card.VALUE_OPTIONS[self.value],
                             Card.SUIT_OPTIONS[self.suit])

    def _play_card(self):
        
        # Update the status message with the clicked card.
        GameState.STATUS_TEXT.set(self.card_name())
        Card.CANVAS.update()

        # Play that card via the trick object.
        self.player_hand.game_state.trick.play_card(self)

        # Disable the click function for the card.
        self.disable_click()

    def disable_click(self):
        if not self.image_shape:
            return
        Card.CANVAS.tag_bind(self.image_shape, '<Button-1>', lambda X: None)

    def enable_click(self):
        Card.CANVAS.tag_bind(self.image_shape, '<Button-1>', 
                             lambda X: self._play_card())

    def hide(self):
        # Sets the card to be face down.
        self.face_up = False
        img_filename = Card.BACK_IMG_FILENAME

        # Create the gif image and assign it to the shape.
        self.photo_image = PhotoImage(
            file=os.path.join(Card.IMG_PATH, img_filename))
        Card.CANVAS.itemconfig(self.image_shape, image=self.photo_image)

    def show(self):
        # Sets the card to be face up.
        self.face_up = True
        img_filename = self.suit + str(self.value) + '.gif'

        # Create the gif image and assign it to the shape.
        self.photo_image = PhotoImage(
            file=os.path.join(Card.IMG_PATH, img_filename))
        Card.CANVAS.itemconfig(self.image_shape, image=self.photo_image)

    def toggle(self):
        # Flips the card over.  Assumes the card has already been drawn.

        # Create the filename.
        if self.face_up == True:
            img_filename = Card.BACK_IMG_FILENAME
        else:
            img_filename = self.suit + str(self.value) + '.gif'

        # Create the gif image and assign it to the shape.
        self.photo_image = PhotoImage(
            file=os.path.join(Card.IMG_PATH, img_filename))
        Card.CANVAS.itemconfig(self.image_shape, image=self.photo_image)

        # Toggle the face_up value.
        self.face_up = not self.face_up

    def __str__(self):
        # Return a string used for sorting.
        if self.value < 10:
            return self.suit + '0' + str(self.value)
        else:
            return self.suit + str(self.value)


class Deck:

    # Constructor.
    def __init__(self):
        self.reset_deck()

    def reset_deck(self):

        # Build a deck of cards.
        self.cards = []
        for suit in Card.SUIT_OPTIONS.keys():
            for value in Card.VALUE_OPTIONS.keys():
                self.cards += [Card(suit, value)]

        # Shuffle the deck.
        random.shuffle(self.cards)

    def deal_card(self):
        # Remove the top card from the deck and return that card.
        return self.cards.pop(0)


class PlayerHand:

    CARD_SPACING = 25

    # Constructor.
    def __init__(self, player_name, upper_left_coords, game_state):

        # Reference to the game_state.
        self.game_state = game_state

        # Basic player info.
        self.player_name = player_name

        # Graphical location of the hand.
        self.coords = upper_left_coords

        self.reset_hand()

    def add_card(self, card):
        # Add the card to this hand, and let the card know it's in this hand.
        self.cards += [card]
        card.player_hand = self

    def play_card(self, card):

        # Make sure this card is in the hand.
        assert card in self.cards

        # Remove the card from this hand and return the card.
        card.player_hand = None
        return self.cards.pop(self.cards.index(card))
        
    def hide_cards(self):
        # Make all the cards in this hand face down.
        for card in self.cards:
            card.hide()
            card.disable_click()

    def show_cards(self):
        # Make all the cards in this hand face up.
        for card in self.cards:
            card.show()
            card.enable_click()

    def take_trick(self, cards_list):
        self.taken_cards += cards_list

    def draw_hand(self, is_vertical=False):
        x, y = self.coords

        # Sort the cards.
        self.cards = sorted(self.cards, key=str, reverse=True)

        # Cyle through and draw each card.
        for card in self.cards:
            card.draw(x, y)

            # Increment the appropriate dimension.
            if is_vertical:
                y += PlayerHand.CARD_SPACING
            else:
                x += PlayerHand.CARD_SPACING

    def reset_hand(self):
        # Empty list to track cards in the hand.
        self.cards = []

        # Empty list to track cards taken.
        self.taken_cards = []

    def has_suit(self, suit):
        
        # Make sure this is a valid suit.
        assert suit in Card.SUIT_OPTIONS

        # Loop through the cards and return true if we find the suit,
        # return False if we get the end without finding it.
        for card in self.cards:
            if card.suit == suit:
                return True
        return False


class Trick:
    ''' Class that holds the played cards in the middle. '''

    # Constructor.
    def __init__(self, canvas_width, canvas_height, game_state):

        # Store a reference to the game state.
        self.game_state = game_state

        # Card dimensions.
        CARD_WIDTH = 70
        CARD_HEIGHT = 96

        # Set the middle coordinates for the played cards.
        x_mid = (canvas_width / 2) - (CARD_WIDTH / 2)
        y_mid = (canvas_height / 2) - (CARD_HEIGHT / 2)
        
        # Store them in a list of coordinate tuples.  Starts with the top-most
        # card and moves clockwise from there.
        self.card_positions = [
            (x_mid, y_mid - (CARD_HEIGHT / 2)),
            (x_mid + (CARD_WIDTH / 2), y_mid),
            (x_mid, y_mid + (CARD_HEIGHT / 2)),
            (x_mid - (CARD_WIDTH / 2), y_mid)
        ]

        # Played cards.
        self.cards = []

    def new_trick(self, lead_position):
        # Empty the cards and set the lead position.
        self.cards = [None, None, None, None]
        self.lead_position = lead_position
        self.turn = lead_position

        # Hide all the players' cards, then show the lead_position's cards.
        self.game_state.hide_hands()
        self.game_state.players[lead_position].show_cards()

    def evaluate_trick(self):
        
        # Make sure the trick is really over.
        assert None not in self.cards
        assert self.game_state.trump is not None

        print 'Trump is', self.game_state.trump

        # Check for highest trump.
        highest_trump = None
        for card in self.cards:
            if card.suit == self.game_state.trump:
                if highest_trump:
                    if card.value > highest_trump.value:
                        highest_trump = card
                else:
                    highest_trump = card

        # Check for cards of the lead suit with a higher value than the lead.
        lead_card = self.cards[self.lead_position]

        print '\nCards taken:'
        winner = lead_card
        for card in self.cards:
            print card.card_name(),
            card.undraw()
            if card.suit == lead_card.suit:
                if card.value > winner.value:
                    winner = card

        if highest_trump:
            print 'Trumped -',
            winner = highest_trump

        print 'Winner:', winner.card_name()

        # Assign card to the winner's taken stack.
        winning_player = self.game_state.players[self.cards.index(winner)]
        winning_player.take_trick(self.cards)

        # Check if winner has any cards left to play.
        if winning_player.cards:
            # Start new trick with winner leading off
            self.new_trick(self.cards.index(winner))
        else:
            # Evaluate the hand.
            self.game_state.evaluate_hand()


    def next_turn(self):
        # If the trick is over, process the results.
        if None not in self.cards:
            self.evaluate_trick()
            return
        
        # Increment the turn.
        self.game_state.players[self.turn].hide_cards()
        self.turn = (self.turn + 1) % 4
        self.game_state.players[self.turn].show_cards()        

    def get_lead_suit(self):
        # Pull out the lead card's suit and return it.
        lead_card = self.cards[self.lead_position]
        if lead_card:
            return lead_card.suit
        else:
            return None

    def is_legal_play(self, card):
        ''' Returns the True if the play was legal, 
        otherwise returns False. '''

        # Get the player index.
        player_index = self.get_player_index(card.player_hand)

        # If we're leading, it's a legal play.
        if self.lead_position == player_index:
            return True

        # If the player doesn't have the lead suit, any play is legal.
        if not card.player_hand.has_suit(self.get_lead_suit()):
            return True

        # Must either trump in or follow suit, otherwise it's not legal.
        if card.suit == self.get_lead_suit():
            return True
        if card.suit == self.game_state.trump:
            return True
        return False

    def play_card(self, card):
        
        # Grab the player.
        player = card.player_hand

        # Make sure this is a legal play, complain and break out if not.
        if not self.is_legal_play(card):
            tk_msg_box.showinfo('Illegal', 'Illegal play.  Choose another card.')
            return

        print card.suit, card.value

        # Get the player index.
        player_index = self.get_player_index(player)

        # Pull out the card from the hand and put it in the trick.
        self.cards[player_index] = player.play_card(card)

        # Figure out the end postion.
        end_x, end_y = self.card_positions[player_index]
        start_x, start_y = card.coords

        # Set up animation values.
        total_steps = 12

        # Calculate the step size for x and y.
        step_x = float(end_x - start_x) / float(total_steps)
        step_y = float(end_y - start_y) / float(total_steps)

        # Move the card to the top of the canvas stack, so it's
        # drawn above the other cards.
        Card.CANVAS.tag_raise(card.image_shape)
        
        # Animate the move.  Updating the canvas takes long enough that we
        # don't need to build in any delay time between little moves.
        for t in range(0, total_steps):
            Card.CANVAS.move(card.image_shape, step_x, step_y)
            Card.CANVAS.update()

        # If trump hasn't been assigned yet, this must be the first card of
        # the hand.
        if self.game_state.trump is None:
            self.game_state.trump = card.suit

        # Pass the turn to the next player.
        self.next_turn()

    def get_player_index(self, player):
        return self.game_state.players.index(player)


class GameState:
    ''' Class where we'll store the entire game state. '''

    # Game config numbers.
    HAND_SIZE = 6
    POINTS_TO_WIN = 21

    # Reference to status bar text where we'll print updates.
    STATUS_TEXT = None
    COMMANDS_FRAME = None
    BID_FRAME = None

    # Constructor.
    def __init__(self, canvas_width, canvas_height):

        # Create a reusable trick.
        self.trick = Trick(canvas_width, canvas_height, self)

        self.deck = Deck()
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Calculate some positions used in hand positioning.
        x_center_coords = \
            (canvas_width / 2) - ((5 * PlayerHand.CARD_SPACING + 70) / 2)
        y_center_coords = \
            (canvas_height / 2) - ((5 * PlayerHand.CARD_SPACING + 96) / 2)

        # Set the coords of the hands.
        coords = [
            (x_center_coords, 10),
            (canvas_width - 80, y_center_coords),
            (x_center_coords, canvas_height - 110),
            (10, y_center_coords)
        ]

        self.players = [
            PlayerHand('Chad', coords[0], self),
            PlayerHand('Kyle', coords[1], self),
            PlayerHand('Sam', coords[2], self),
            PlayerHand('Lamar', coords[3], self)
        ]
        self.score = [0, 0]

        # References to trump suit and dealer.
        self.trump = None
        self.dealer_position = None

        # Bid is player_index, bid_amount.
        self.bid = [None, None]
        self.bid_position = None

    def evaluate_hand(self):
        """ Evaluate the hand based on the cards the players have taken. """
        # Tally trump points.
        high, low = [None, 0], [None, 14]
        game = [0, 0]
        points = [0, 0]

        for i in range(0, len(self.players)):
            team_index = i % 2
            for card in self.players[i].taken_cards:
                if card.suit == self.trump:
                    # Check for high and low.
                    if not high[0]:
                        high = (team_index, card.value)
                    
                    if card.value > high[1]:
                        high = (team_index, card.value)
                    
                    if card.value < low[1]:
                        low = (team_index, card.value)
                    
                    # Check for Jack.
                    if card.value == 11:
                        print 'Jack taken by Team', team_index + 1
                        points[team_index] += 1

                # Tally points toward game.
                if card.value >= 10:
                    game[team_index] += card.game_value()

        # Add game point - not awarded if tied.
        print 'Team 1 Game Score:', game[0]
        print 'Team 2 Game Score:', game[1]

        if game[0] > game[1]:
            print 'Team 1 awarded Game Point.'
            points[0] += 1
        elif game[0] < game[1]:
            print 'Team 2 awarded Game Point.'
            points[1] += 1
        else:
            print 'No Game Point awarded.'

        print 'Team {0} takes high trump.'.format((high[0] % 2) + 1)
        print 'Team {0} takes low trump.'.format((low[0] % 2) + 1)

        # Add high and low.
        points[(high[0] % 2)] += 1
        points[(low[0] % 2)] += 1

        # Check tallies against the bid.
        if points[(self.bid[0] % 2)] < self.bid[1]:
            points[(self.bid[0] % 2)] = (0 - self.bid[1])

        # Assign points to teams.
        for i in range(0, len(self.score)):
            self.score[i] += points[i]
            print 'Team {0} Hand Score: {1}'.format(i + 1, points[i])
            print 'Team {0} Total Score: {1}'.format(i + 1, self.score[i])

        # TODO Check if victory conditions have been met.

        # Deal another hand if game continues.
        self.dealer_position = (self.dealer_position + 1) % 4
        self.deal_hands(self.dealer_position)

    def set_player_bid(self, player_index, bid):
        if bid:
            self.bid = [player_index, bid]

        print 'Player', player_index + 1, 'bids', bid

        if self.dealer_position == player_index:
            msg_text = '{0} Bid taken by Player {1}'.format(self.bid[1], 
                                                            self.bid[0] + 1)

            # Start new trick.
            self.BID_FRAME.hide()
            self.COMMANDS_FRAME.show()
            self.trump = None
            self.bid[1] = None
            self.trick.new_trick(self.bid[0])
        else:
            self.bid_position = (self.bid_position + 1) % 4
            self.ask_for_player_bid(self.bid_position)
            msg_text = 'Player', player_index + 1, 'bids', bid

        GameState.STATUS_TEXT.set(msg_text)
        Card.CANVAS.update()

    def ask_for_player_bid(self, player_index):
        GameState.COMMANDS_FRAME.hide()

        # Hide all hands, then show this player's hand.
        self.hide_hands()
        self.players[player_index].show_cards()
        for card in self.players[player_index].cards:
            card.disable_click()

        # Figure out the minimum bid
        if self.bid[1] == None:
            min_bid = 2
        elif player_index == self.dealer_position:
            min_bid = self.bid[1]
        else:
            min_bid = self.bid[1] + 1

        # Activate allowed bid buttons.
        for i in range(0, len(GameState.BID_FRAME.buttons)):
            GameState.BID_FRAME.disable_button(i)
            if (i + 2) >= min_bid:
                GameState.BID_FRAME.enable_button(i)

        # Enable the pass button if needed.
        if player_index != self.dealer_position:
            self.BID_FRAME.enable_button(3)
        elif self.bid[1] == None:
            print 'Dealer cannot pass.'

        self.BID_FRAME.frame['text'] = 'Player {0} Bid'.format(self.bid_position + 1)
        self.BID_FRAME.show()

    def deal_hands(self, dealer_position):

        # Clear out the previous hand.
        self.clear_hands()

        # Loop through the players, dealing out one card at a time.
        # NOTE: This could be modified to do a 3-at-a-time deal.
        cards_dealt = 0
        while cards_dealt < GameState.HAND_SIZE:
            for player in self.players:
                player.add_card(self.deck.deal_card())
            cards_dealt += 1

        # Draw the hands.
        vert = False
        for player in self.players:
            player.draw_hand(is_vertical=vert)
            vert = not vert
        self.dealer_position = dealer_position
        
        # Start the bidding.
        self.bid_position = (dealer_position + 1) % 4
        self.ask_for_player_bid(self.bid_position)

    def hide_hands(self):
        for player in self.players:
            player.hide_cards()

    def clear_hands(self):
        # Clear out all the stored data.
        self.deck.reset_deck()
        for player in self.players:
            player.reset_hand()

