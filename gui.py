import Tkinter as tk


class GuiFrame(object):

    # Configuration options for each LabelFrame
    # best to set these in the module you're using
    # to call this class.
    PROPAGATE = False
    RELIEF = tk.FLAT
    LABELANCHOR = tk.N
    WIDTH = 300
    HEIGHT = 500

    # NOTE: these options MUST be overridden.
    PARENT_WIDGET = None
    TK_ROOT = None

    def __init__(self, text='Title Text', width=WIDTH, height=HEIGHT, 
                 relief=RELIEF, labelanchor=LABELANCHOR, **kwargs):
        # Hold on the text in a separate var, for ease of use.
        self.text = text

        # The tkinter frame.
        self.frame = tk.LabelFrame(
            GuiFrame.PARENT_WIDGET,
            text=text, 
            labelanchor=labelanchor,
            relief=relief,
            width=width, 
            height=height
        )

        self.frame.grid_propagate(GuiFrame.PROPAGATE)

    def show(self):
        self.frame.pack(side=tk.TOP)
        self.update_gui()

    def hide(self):
        self.frame.pack_forget()
        self.update_gui()

    def update_gui(self):
        GuiFrame.TK_ROOT.update_idletasks()


class StatusFrame(GuiFrame):

    def __init__(self, *args, **kwargs):
        super(StatusFrame, self).__init__(*args, **kwargs)

        # Set up our interior text.
        self.status_text = tk.StringVar()
        self.status_text.set('Default status.')
        if 'status_text' in kwargs:
            self.status_text.set(kwargs['status_text'])
        
        self.text_label = tk.Label(
            self.frame, 
            textvariable=self.status_text,
            font=10
        )

    def show(self):
        self.frame.pack(side=tk.BOTTOM, fill='both', expand='yes')
        self.text_label.pack(fill='both')

        # Force the screen to update.
        GuiFrame.TK_ROOT.update_idletasks()


class ButtonFrame(GuiFrame):

    def __init__(self, *args, **kwargs):
        '''
        NOTE: The child_frames of this frame are not children widgets
        in the Tkinter sense, just in a menu sense.  All frames will
        be Tkinter children of the PARENT_WIDGET specified in GuiFrame.
        '''
        super(ButtonFrame, self).__init__(*args, **kwargs)

        self.buttons = []

        # Use these to keep track of the menu tree.
        self.parent_frame = None
        self.child_frames = []

    def show(self):
        self.show_buttons()
        super(ButtonFrame, self).show()

    def hide(self):
        self.hide_buttons()
        super(ButtonFrame, self).hide()

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
            self.buttons.append(tk.Button(self.frame, text=text, command=command))
        else:
            self.buttons.append(tk.Button(self.frame, text=text))

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
            button.grid(row=i, sticky=tk.W)
            i = i + 1

    def hide_buttons(self):
        ''' Ungrid all the buttons. '''
        for button in self.buttons:
            button.grid_forget()

    def disable_button(self, button_index):
        ''' Deactivate a button at a given index. '''
        self.buttons[button_index].configure(state=tk.DISABLED)

    def enable_button(self, button_index):
        ''' Activate a button at a given index. '''
        self.buttons[button_index].configure(state=tk.NORMAL)

    def disable_button_by_text(self, search_text):
        ''' Deactivate the first button with given text. '''
        target_button = None
        for button in self.buttons:
            if button.cget('text') == search_text:
                target_button = button
                break

        # Deactivate it if found.
        if target_button:
            target_button.configure(state=tk.DISABLED)
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
            target_button.configure(state=tk.NORMAL)
        else:
            print 'Could not find button with text "{0}".'.format(search_text)
