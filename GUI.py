from tkinter import *
from DataAccess import APIAccess
from tkinter.ttk import Separator
from Examples import RNN

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
        label = Label(upperframe, text="AI-Forecast Application\n" + "by\n" + "Jason, Swatt, and Tiger", bg='#525453', font=100)
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
        # make frames
        upperframe = Frame(root, bg='#525453')
        upperframe.place(relx=0, rely=.05, relwidth=1, relheight=.95)
        #make lines

        # make labels
        title = Label(upperframe, text="Train", bg='#525453', font=100)
        title.place(relx=.5, rely=.02)
        source_label = Label(upperframe, bg='#525453')
        source_label.place(relx=0.05, rely=.2)
        input_label = Label(upperframe, text="Choose Input Source:", bg='#525453', font=100)
        input_label.place(relx=0, rely=.02, relwidth=.2, relheight=.1)
        output_label = Label(upperframe, text="", bg='#525453', font=100)
        output_label.place(relx=.75, rely=.1, relwidth=.2, relheight=.1)
        #make buttons
        v = StringVar()
        historic_button = Radiobutton(upperframe, variable=v, value="hist", text="Historic Data", borderwidth=5, bg='#525453', fg='black', command=lambda: historic_label(self))
        historic_button.place(relx=.05, rely=.1)
        user_button = Radiobutton(upperframe, variable=v, value="user", text="User Data", borderwidth=5, bg='#525453', fg='black', command=lambda: user_label(self))
        user_button.place(relx=.175, rely=.1)
        # compound_button = Radiobutton(upperframe, text="User and Historic Data", borderwidth=5, bg='#525453', fg='#d4d5d6', command=lambda: compound_label(self))
        # compound_button.place(relx=.3, rely=.1)
        run_button = Button(upperframe, text="Run", borderwidth=5, bg='#525453', fg='#d4d5d6',command=lambda: run_train(self))
        run_button.place(relx=.75, rely=.1)

        def historic_label(self):
            source_label.config(text="Use historic data to train the model.")
            years_label = Label(text="Select the number of years to retrieve historical data from:", bg='#525453', fg="white")
            years_label.place(relx=.05, rely=.3)
            variable = StringVar(upperframe)
            variable.set("one")  # default value
            years_dropdown = OptionMenu(root, variable, "one", "two", "three", "four", "five", "six")
            years_dropdown.place(relx=.05, rely=.35)

        def user_label(self):
            source_label.config(text="Use user data to train the model.")
            #blocks out dropdown
            label = Label(text="            ", bg="#525453")
            label.place(relx=.05, rely=.3, relwidth=.33, relheight=.25)

        # def compound_label(self):
        #     source_label.config(text="Use a combination of historic data and user data to train the model.")
        #     #blocks out dropdown
        #     label = Label(text="            ", bg="#525453")
        #     label.place(relx=.05, rely=.3, relwidth=.33, relheight=.25)

        def run_train(self):
            output_label.config(text="Training...")
            test = RNN.RNN
            test.runRNN(test)


    # load items for Testing page
    def init_Test(self):
        # changing the title of our master widget
        self.master.title("Test Menu")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # make canvas
        canvas = Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()
        # make frames
        upperframe = Frame(root, bg='#525453')
        upperframe.place(relx=0, rely=.05, relwidth=1, relheight=.95)
        # make labels
        title = Label(upperframe, text="Test", bg='#525453', font=100)
        title.place(relx=.5, rely=.02)
        source_label = Label(upperframe, bg='#525453')
        source_label.place(relx=0.05,rely=.2)
        input_label = Label(upperframe, text="Choose Input Source:", bg='#525453', font=100)
        input_label.place(relx=0, rely=.02, relwidth=.2, relheight=.1)
        str_out = StringVar()
        output_label = Label(upperframe, textvariable=str_out, bg='#525453')
        output_label.place(relx=.45, rely=.2)
        #make buttons
        v = StringVar()
        current_button = Radiobutton(upperframe, text="Current", variable=v, value="current", borderwidth=5, bg='#525453', fg='black', command=lambda: current_label(self))
        current_button.place(relx=.05, rely=.1)
        manual_button = Radiobutton(upperframe, text="Manual", variable=v, value="manual", borderwidth=5, bg='#525453', fg='black', command=lambda: manual_label(self))
        manual_button.place(relx=.15, rely=.1)
        run_button = Button(upperframe, text="Run", borderwidth=5, bg='#525453', fg='#d4d5d6', command=lambda: run_test(self))
        run_button.place(relx=.75, rely=.1)

        # entry boxes
        # hourbox = Entry(upperframe)
        # hourbox.place(relx=.15, rely=.2)
        #
        # daybox = Entry(upperframe)
        # daybox.place(relx=.15, rely=.25)
        #
        # monthbox = Entry(upperframe)
        # monthbox.place(relx=.15, rely=.3)
        #
        # tempbox = Entry(upperframe)
        # tempbox.place(relx=.15, rely=.35)
        #
        # temp_minbox = Entry(upperframe)
        # temp_minbox.place(relx=.15, rely=.4)
        #
        # temp_maxbox = Entry(upperframe)
        # temp_maxbox.place(relx=.15, rely=.45)
        #
        # pressurebox = Entry(upperframe)
        # pressurebox.place(relx=.15, rely=.5)
        #
        # humiditybox = Entry(upperframe)
        # humiditybox.place(relx=.15, rely=.55)
        #
        # windspeedbox = Entry(upperframe)
        # windspeedbox.place(relx=.15, rely=.6)
        #
        # winddirbox = Entry(upperframe)
        # winddirbox.place(relx=.15, rely=.65)



        def current_label(self):
            source_label.config(text="Use current data to make a prediction.")
            self.current = True # set boolean to true to let controller know to use current data later

        def manual_label(self):
            source_label.config(text="Use manually inputted data to make a prediction.")
            self.current = False # set boolean to false to know to use manually inputted data

        def run_test(self):
            api_access = APIAccess.APIAccess
            api_access.getCurrent(api_access)
            str_erie = "Erie: " + str(api_access.year) + ", " + str(api_access.month) + ", " + str(api_access.day) + ", " + str(api_access.hour)
            str_erie = str_erie + ", " + str(api_access.temp) + ", " + str(api_access.min_temp) + ", " + str(api_access.max_temp) + ", "
            str_erie = str_erie + str(api_access.humidity) + ", " + str(api_access.pressure) + ", " + str(api_access.wind_speed) + ", " + str(api_access.wind_dir)

            str_city1 = "Location 1: " + str(api_access.year_1) + ", " + str(api_access.month_1) + ", " + str(api_access.day_1) + ", " + str(api_access.hour_1)
            str_city1 = str_city1 + ", " + str(api_access.temp_1) + ", " + str(api_access.min_temp_1) + ", " + str(api_access.max_temp_1) + ", "
            str_city1 = str_city1 + str(api_access.humidity_1) + ", " + str(api_access.pressure_1) + ", " + str(api_access.wind_speed_1) + ", " + str(api_access.wind_dir_1)

            str_city2 = "Location 2: " + str(api_access.year_2) + ", " + str(api_access.month_2) + ", " + str(api_access.day_2) + ", " + str(api_access.hour_2)
            str_city2 = str_city2 + ", " + str(api_access.temp_2) + ", " + str(api_access.min_temp_2) + ", " + str(api_access.max_temp_2) + ", "
            str_city2 = str_city2 + str(api_access.humidity_2) + ", " + str(api_access.pressure_2) + ", " + str(api_access.wind_speed_2) + ", " + str(api_access.wind_dir_2)

            str_city3 = "Location 3: " + str(api_access.year_3) + ", " + str(api_access.month_3) + ", " + str(api_access.day_3) + ", " + str(api_access.hour_3)
            str_city3 = str_city3 + ", " + str(api_access.temp_3) + ", " + str(api_access.min_temp_3) + ", " + str(api_access.max_temp_3) + ", "
            str_city3 = str_city3 + str(api_access.humidity_3) + ", " + str(api_access.pressure_3) + ", " + str(api_access.wind_speed_3) + ", " + str(api_access.wind_dir_3)

            str_out.set("Year, Month, Day, Hour, Temp, Min Temp, Max Temp, Humidity, Pressure, Wind Speed, Wind Direction" + "\n" + str_erie + "\n" + str_city1 + "\n" + str_city2 + "\n" + str_city3)




    def client_exit(self):
        exit()


root = Tk()
root.geometry("1000x600")
app = Window(root)
root.mainloop()
