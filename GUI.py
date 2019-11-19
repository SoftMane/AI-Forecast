from tkinter import *

HEIGHT = 600
WIDTH = 1000
current = True

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
# Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("Main Menu")


        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # make canvas
        canvas = Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()
        # make frame
        upperframe = Frame(root, bg='#525453')
        upperframe.place(relx=0, rely=.05, relwidth=1, relheight=.95)
        # make label
        label = Label(upperframe, text="AI-Forecast", bg='#525453', font=100)
        label.place(relx=0, rely=0, relwidth=1, relheight=.4)

        # NavBar
        # nav frame
        nav = Frame(root, bg='gray')
        nav.place(relx=0, rely=0, relwidth=1, relheight=.05)
        # nav buttons
        indexNav = Button(nav, text="Main", borderwidth=5, bg='#525453', fg='#d4d5d6', command=self.init_window)
        indexNav.place(relx=0, rely=0, relwidth=.1, relheight=1)
        testNav = Button(nav, text="Test", borderwidth=5, bg='#525453', fg='#d4d5d6', command=self.init_Test)
        testNav.place(relx=.1, rely=0, relwidth=.1, relheight=1)
        trainNav = Button(nav, text="Train", borderwidth=5, bg='#525453', fg='#d4d5d6', command=self.init_Train)
        trainNav.place(relx=.2, rely=0, relwidth=.1, relheight=1)

    # load items for Training page
    def init_Train(self):
        # changing the title of our master widget
        self.master.title("Train Menu")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # make canvas
        canvas = Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()
        # make frame
        upperframe = Frame(root, bg='#525453')
        upperframe.place(relx=0, rely=.05, relwidth=1, relheight=.95)
        # make label
        label = Label(upperframe, text="Train", bg='#525453', font=100)
        label.place(relx=0, rely=0, relwidth=1, relheight=.4)

    # load items for Testing page
    def init_Test(self):
        # changing the title of our master widget
        self.master.title("Test Menu")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # make canvas
        canvas = Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()
        # make frame
        upperframe = Frame(root, bg='#525453')
        upperframe.place(relx=0, rely=.05, relwidth=1, relheight=.95)
        # make label
        source_label = Label(upperframe, bg='#525453')
        source_label.place(relx=0.05,rely=.2)
        label = Label(upperframe, text="Choose Input Source:", bg='#525453', font=100)
        label.place(relx=0, rely=0, relwidth=.2, relheight=.1)
        current_button = Button(upperframe, text="Current", borderwidth=5, bg='#525453', fg='#d4d5d6', command=lambda: current_label(self))
        current_button.place(relx=.05, rely=.1)
        manual_button = Button(upperframe, text="Manual", borderwidth=5, bg='#525453', fg='#d4d5d6', command=lambda: manual_label(self))
        manual_button.place(relx=.15, rely=.1)

        def current_label(self):
            source_label.config(text="Use current data to make a prediction.")
            self.current = True # set boolean to true to let controller know to use current data later

        def manual_label(self):
            source_label.config(text="Use manually inputted data to make a prediction.")
            self.current = False # set boolean to false to know to use manually inputted data


    def client_exit(self):
        exit()


root = Tk()
root.geometry("1000x600")
app = Window(root)
root.mainloop()
