from Tkinter import *

class ButtonFrame:

    # configuration options for each LabelFrame
    # best to set these in the module you're using
    # to call this class
    PROPAGATE = False
    RELIEF = FLAT
    LABELANCHOR = N
    
    # NOTE: these options should be overridden 
    # in your calling code
    WIDTH = 300
    HEIGHT = 500

    # NOTE: these options MUST be overridden
    PARENT_WIDGET = None
    TK_ROOT = None

    # constructor
    def __init__(self, text):
        '''
        NOTE: The child_frames of this frame are not children widgets
        in the Tkinter sense, just in a menu sense.  All frames will
        be Tkinter children of the PARENT_WIDGET specified above.
        '''
        
        # hold on the text in a separate var, for ease of use
        self.text = text

        # the tkinter frame
        self.frame = LabelFrame(ButtonFrame.PARENT_WIDGET,
                                text=text, 
                                labelanchor=ButtonFrame.LABELANCHOR,
                                relief=ButtonFrame.RELIEF,
                                width=ButtonFrame.WIDTH, 
                                height=ButtonFrame.HEIGHT)

        self.frame.grid_propagate(ButtonFrame.PROPAGATE)

        self.buttons = []

        # use these to keep track of the menu tree
        self.parent_frame = None
        self.child_frames = []

    # show this frame
    def show(self):
        self.show_buttons()
        self.frame.pack(side=TOP)

        # force the screen to update
        ButtonFrame.TK_ROOT.update_idletasks()

    # hide this frame
    def hide(self):
        self.hide_buttons()
        self.frame.pack_forget()

        # force the screen to update
        ButtonFrame.TK_ROOT.update_idletasks()

    # show child frame and hide self
    def show_child(self, child_index):
        self.hide()
        self.child_frames[child_index].show()

    # show parent and hide self
    def show_parent(self):
        self.hide()
        self.parent_frame.show()

    # add the child frame to the list
    # and set the child's parent to us
    def add_child(self, child_frame):
        self.child_frames.append(child_frame)
        child_frame.parent_frame = self

    # deletes all the children frames
    def delete_children(self):
        
        # hide and destroy each child
        for child in self.child_frames:
            child.hide()
            child.frame.destroy()

        # set child_frames to an empty list
        self.child_frames = []

    # find a reference to a child frame based on the text label
    # returns either a reference to the frame or None
    def get_child_by_text(self, search_text):
        return_frame = None
        for frame in self.child_frames:
            if frame.text == search_text:
                return_frame = frame
                break
        return return_frame

    # add a button to the end of the buttons list
    # NOTE: does not display said button
    def add_button(self, text, command=None):   
        if command:
            self.buttons.append(Button(self.frame, text=text, command=command))
        else:
            self.buttons.append(Button(self.frame, text=text))

    # insert a button at the specified index, shifts elements to the right
    def insert_button(self, index, text, command=None):
        if command:
            self.buttons.insert(index, Button(self.frame, text=text, command=command))
        else:
            self.buttons.insert(index, Button(self.frame, text=text))

    # remove a button from anywhere in the buttons list - does not redraw buttons
    def remove_button(self, index):

        # make sure the index is in bounds
        if index < len(self.buttons):
            self.buttons.pop(index)
            # TODO actually delete the button, don't just remove it from the list
        else:
            print str(index) + ' out of bounds.  self.buttons has length of ' + str(len(self.buttons))

    # grid all the buttons associated with this frame
    def show_buttons(self):
        i = 0
        for button in self.buttons:
            button.grid(row=i, sticky=W)
            i = i + 1

    # ungrid all the buttons
    def hide_buttons(self):
        for button in self.buttons:
            button.grid_forget()

    # deactivate a button at a given index
    def disable_button(self, button_index):
        self.buttons[button_index].configure(state=DISABLED)

    # activate a button at a given index
    def enable_button(self, button_index):
        self.buttons[button_index].configure(state=NORMAL)

    # deactivate the first button with given text
    def disable_button_by_text(self, search_text):
        target_button = None
        for button in self.buttons:
            if button.cget('text') == search_text:
                target_button = button
                break

        # deactivate it if found
        if target_button:
            target_button.configure(state=DISABLED)
        else:
            print 'Could not find button with text "' + search_text + '".'

    # activate the first button with given text
    def enable_button_by_text(self, search_text):
        target_button = None
        for button in self.buttons:
            if button.cget('text') == search_text:
                target_button = button
                break

        # activate it if found
        if target_button:
            target_button.configure(state=NORMAL)
        else:
            print 'Could not find button with text "' + search_text + '".'

