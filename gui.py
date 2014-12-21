from Tkinter import *

class ButtonFrame:

    # Configuration options for each LabelFrame
    # best to set these in the module you're using
    # to call this class.
    PROPAGATE = False
    RELIEF = FLAT
    LABELANCHOR = N
    
    # NOTE: these options should be overridden 
    # in your calling code.
    WIDTH = 300
    HEIGHT = 500

    # NOTE: these options MUST be overridden.
    PARENT_WIDGET = None
    TK_ROOT = None

    def __init__(self, text):
        '''
        NOTE: The child_frames of this frame are not children widgets
        in the Tkinter sense, just in a menu sense.  All frames will
        be Tkinter children of the PARENT_WIDGET specified above.
        '''
        
        # Hold on the text in a separate var, for ease of use.
        self.text = text

        # The tkinter frame.
        self.frame = LabelFrame(ButtonFrame.PARENT_WIDGET,
                                text=text, 
                                labelanchor=ButtonFrame.LABELANCHOR,
                                relief=ButtonFrame.RELIEF,
                                width=ButtonFrame.WIDTH, 
                                height=ButtonFrame.HEIGHT)

        self.frame.grid_propagate(ButtonFrame.PROPAGATE)

        self.buttons = []

        # Use these to keep track of the menu tree.
        self.parent_frame = None
        self.child_frames = []

    def show(self):
        self.show_buttons()
        self.frame.pack(side=TOP)

        # Force the screen to update.
        ButtonFrame.TK_ROOT.update_idletasks()

    def hide(self):
        self.hide_buttons()
        self.frame.pack_forget()

        # Force the screen to update.
        ButtonFrame.TK_ROOT.update_idletasks()

    def show_child(self, child_index):
        self.hide()
        self.child_frames[child_index].show()

    def show_parent(self):
        self.hide()
        self.parent_frame.show()

    def add_child(self, child_frame):
        # Add the child frame to the list and set the child's parent to us.
        self.child_frames.append(child_frame)
        child_frame.parent_frame = self

    def delete_children(self):
        # Hide and destroy each child.
        for child in self.child_frames:
            child.hide()
            child.frame.destroy()
        self.child_frames = []

    def get_child_by_text(self, search_text):
        ''' Find a reference to a child frame based on the text label
        returns either a reference to the frame or None. '''
        return_frame = None
        for frame in self.child_frames:
            if frame.text == search_text:
                return_frame = frame
                break
        return return_frame

    def add_button(self, text, command=None):   
        ''' Add a button to the end of the buttons list.
        NOTE: does not display said button. '''
        if command:
            self.buttons.append(Button(self.frame, text=text, command=command))
        else:
            self.buttons.append(Button(self.frame, text=text))

    def insert_button(self, index, text, command=None):
        ''' Insert a button at the specified index, 
        shifts elements to the right. '''
        if command:
            self.buttons.insert(
                index, 
                Button(self.frame, text=text, command=command)
            )
        else:
            self.buttons.insert(index, Button(self.frame, text=text))

    def remove_button(self, index):
        ''' Remove a button from anywhere in the buttons list. 
        NOTE: does not redraw buttons. '''

        # Make sure the index is in bounds.
        if index < len(self.buttons):
            self.buttons.pop(index)
            # TODO actually delete the button, 
            # don't just remove it from the list.
        else:
            print '{0} out of bounds.  self.buttons has length of {1}'.format(
                index, len(self.buttons)
            )

    def show_buttons(self):
        ''' Grid all the buttons associated with this frame. '''
        i = 0
        for button in self.buttons:
            button.grid(row=i, sticky=W)
            i = i + 1

    def hide_buttons(self):
        ''' Ungrid all the buttons. '''
        for button in self.buttons:
            button.grid_forget()

    def disable_button(self, button_index):
        ''' Deactivate a button at a given index. '''
        self.buttons[button_index].configure(state=DISABLED)

    def enable_button(self, button_index):
        ''' Activate a button at a given index. '''
        self.buttons[button_index].configure(state=NORMAL)

    def disable_button_by_text(self, search_text):
        ''' Deactivate the first button with given text. '''
        target_button = None
        for button in self.buttons:
            if button.cget('text') == search_text:
                target_button = button
                break

        # Deactivate it if found.
        if target_button:
            target_button.configure(state=DISABLED)
        else:
            print 'Could not find button with text "{0}".'.format(search_text)

    def enable_button_by_text(self, search_text):
        ''' Activate the first button with given text. '''
        target_button = None
        for button in self.buttons:
            if button.cget('text') == search_text:
                target_button = button
                break

        # Deactivate it if found.
        if target_button:
            target_button.configure(state=NORMAL)
        else:
            print 'Could not find button with text "{0}".'.format(search_text)
