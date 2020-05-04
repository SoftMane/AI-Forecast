import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

import numpy as np

from tensorflow.keras.models import load_model
from DataAccess import APIAccess
########    add   #################
from DataAccess import HistAccess
from DataAccess.HistAccess import HistAccess
from DataAccess.load_data import load_data_class

from Examples import RNN

########################################################################################
# memo:
#       update the city name into, read them from a file,
#       put city selection into a list
#
########################################################################################

HEIGHT = 600
WIDTH = 1000
current = True

############    Global list to store user data #################
storedData = []
cityOption = ["Buffalo", "Cleveland", "Pittsburgh"]
targetCityOption = ["Erie"]
citySelected = []
testCitySelected = []
##############    for city option looping   ######################
tkVarForFileLoop = []
################################################################
######################      load_data     ############################
global data_path
data_path='/Users//Users/tigergoodbread/Downloads/AI-Forecast-master/'

#global train_path
#train_path= "training.pkl"
#global valid_path
#valid_path = "validation.pkl"
#global test_path
#test_path= "testing.pkl"

####################         BatchGenerator     ######################
trainX = []
trainY = []
validX = []
validY = []
testX = []
testY = []

trainXFinal = []
validXFinal = []
testXFinal = []

trainYFinal = []
validYFinal = []
testYFinal = []

###Reference:http://bluegalaxy.info/codewalk/2017/10/14/python-how-to-create-gui-pop-up-windows-with-tkinter/####
def alert_popup(title, message, path):
    """Generate a pop-up window for special messages."""
    root = Tk()
    root.title(title)
    w = 400     # popup window width
    h = 200     # popup window height
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message
    m += '\n'
    m += path
    w = Label(root, text=m, width=120, height=10)
    w.pack()
    b = Button(root, text="Continue", command=root.destroy, width=10)
    b.pack()
    mainloop()


#########################################################################################################
alert_popup("!!!Welcome!!!!", "Senior Design Project:\nTraining AI to Predict Temperature", "Team #11")
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
        label = Label(upperframe, text="Training AI to Predict Temperature\n" + "by\n" + "Jason, Swatt, and Tiger", bg='#525453', fg='white', font=100)
        label.place(relx=0, rely=0, relwidth=1, relheight=.4)

        # NavBar
        # nav frame
        nav = Frame(root, bg='gray')
        nav.place(relx=0, rely=0, relwidth=1, relheight=.05)
        # nav buttons
        indexNav = Button(nav, text="Main", borderwidth=5, bg='white', fg='black', command=self.init_window)
        indexNav.place(relx=0, rely=0, relwidth=.1, relheight=1)
        testNav = Button(nav, text="Test", borderwidth=5, bg='white', fg='black', command=self.init_Test)
        testNav.place(relx=.1, rely=0, relwidth=.1, relheight=1)
        trainNav = Button(nav, text="Train", borderwidth=5, bg='white', fg='black', command=self.init_Train)
        trainNav.place(relx=.2, rely=0, relwidth=.1, relheight=1)

        ##########################                      add                    ##############################
        # exitNav = Button(nav, text="Exit", borderwidth=5, bg='#525453', fg='#d4d5d6', command=self.client_exit)
        # exitNav.place(relx=.8, rely=0, relwidth=.1, relheight=1)
        # userInputNav = Button(nav, text="Create Data", borderwidth=5, bg='#525453', fg='#d4d5d6',command=self.user_input)
        # userInputNav.place(relx=.3, rely=0, relwidth=.1, relheight=1)
        CityOptionNav = Button(nav, text="CityOptions", borderwidth=5, bg='white', fg='black', command=self.expand_Options)
        CityOptionNav.place(relx=.3, rely=0, relwidth=.1, relheight=1)

        # #############################################            Test            #######################################
        # TTNav = Button(nav, text="test_test", borderwidth=5, bg='#525453', fg='#d4d5d6', command=self.test_test)
        # TTNav.place(relx=.7, rely=0, relwidth=.1, relheight=1)



    # load items for Training page
    def init_Train(self):
        # self.init_window().indexNav.config(state=NORMAL)
        # self.init_window().trainNav.config(state=DISABLED)
        # self.init_window().testNav.config(state=NORMAL)
        # self.init_window().CityOptionNav.config(state=NORMAL)
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


        # make labels
        # title = Label(upperframe, text="Train the model", bg='white', fg='black', font=100)
        # title.place(relx=.4, rely=.02)
        source_label = Label(upperframe, bg='#525453')
        source_label.place(relx=0.03, rely=.15)
        input_label = Label(upperframe, text="Choose Input Source:", fg='white', bg='#525453', font=100)
        input_label.place(relx=-.02, rely=.02, relwidth=.2, relheight=.1)
        #output_label = Label(upperframe,text="                        ", bg='#525453', font=100)
        #output_label.place(relx=.5, rely=.2, relwidth=.2, relheight=.2)

        cover_box = Frame(root, bg='#525453', highlightcolor='#525453')
        cover_box.place(relx=.35, rely=.1, relwidth=.6, relheight=.3)
        input_label = Label(upperframe, text="Choose surrounding cities from the list:", fg="white", bg='#525453',
                            font=100)
        input_label.place(relx=.37, rely=.02, relwidth=.3, relheight=.1)

        input_label2 = Label(upperframe, text="Choose a target city from the list:", fg="white", bg='#525453',
                            font=100)
        input_label2.place(relx=.65, rely=.02, relwidth=.3, relheight=.1)

        divide_label = Label(upperframe, text=".....................................................................................................................................................................................................................................................................", fg="white", bg='#525453',
                            font=100)
        divide_label.place(relx=-.0, rely=0.5)

        run_label = Label(upperframe, text="Press the button below to begin training", font="100", bg='#525453',
                          fg='white')
        run_label.place(relx=.1, rely=.57)
        training_label = Label(upperframe, text="Training in progress", font="100", bg='#525453', fg='white')

        #############Ouput Receipt##############
        output_title = Label(upperframe, text="Output:", bg='#525453', fg='white', font=100)
        output_title.place(relx=.5, rely=.55, relwidth=.1, relheight=.1)
        output_label = tkinter.Text(upperframe, height=2, width=30)
        output_label.place(relx=.5, rely=.65, relwidth=.4, relheight=.2)

        #make buttons
        v = StringVar()
        historic_button = Radiobutton(upperframe, variable=v, value="hist", text="Historic Data", borderwidth=5, bg='#525453', fg='white', command=lambda: historic_label(self))
        historic_button.place(relx=.03, rely=.1)
        historic_button.select()
        user_button = Radiobutton(upperframe, variable=v, value="user", text="User Data", borderwidth=5, bg='#525453', fg='grey', command=lambda: user_label(self))
        user_button.config(state=DISABLED)
        user_button.place(relx=.15, rely=.1)

        # compound_button = Radiobutton(upperframe, text="User and Historic Data", borderwidth=5, bg='#525453', fg='#d4d5d6', command=lambda: compound_label(self))
        # compound_button.place(relx=.3, rely=.1)
        run_button = Button(upperframe, text="Run", borderwidth=5, bg='white', fg='black', command=lambda: run_train(self), state=DISABLED)
        run_button.place(relx=0.165, rely=.7, relwidth=.1, relheight=.1)

        # text_label = Label(upperframe, text="Please Select 4 cites from the list", font="100", bg='#525453', fg='#d4d5d6')

        # self.historic_label(self)
        variable1 = StringVar(upperframe)
        variable2 = StringVar(upperframe)
        variable3 = StringVar(upperframe)
        start_year = OptionMenu(root, variable1, "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009",
                                "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "20019")
        end_year = OptionMenu(root, variable2, "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009",
                              "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019")
        future_time = OptionMenu(root, variable3, "2", "4", "8")
        ####################################                  Functionality                ######################################################
        def historic_label(self):
            # input_source_selected = True
            source_label.config(text="This option uses historic data to train the model.")
            years_label = Label(text="Select a year range for historical data:", bg='#525453', fg="white")
            years_label.place(relx=.03, rely=.25)
            run_button.config(state=NORMAL)
            cover_box.destroy()
            surrounding_cities_listbox.config(state=NORMAL)
            target_cities_listbox.config(state=NORMAL)

            variable1.set("not selected")  # default value
            variable2.set("not selected")  # default value
            start_year.place(relx=.03, rely=.3)
            end_year.place(relx=.15, rely=.3)

            global start_year_parameter
            start_year_parameter = variable1
            global end_year_parameter
            end_year_parameter = variable2

            future_label = Label(text="Select a future time (hr):", bg='#525453', fg="white")
            future_label.place(relx=.03, rely=.4)

            variable3.set("not selected")
            future_time.place(relx=.03, rely=.45)

            global future_time_parameter
            future_time_parameter = variable3

        def user_label(self):
            source_label.config(text="this feature is currently unavailable.")

            surrounding_cities_listbox.config(state=DISABLED)
            target_cities_listbox.config(state=DISABLED)
            # source_label.config(text="this option uses user-imported data to train the model.")
            #blocks out dropdown
            label = Label(text="            ", bg="#525453")
            label.place(relx=.03, rely=.25, relwidth=.3, relheight=.29)

        def confirm_selection(self):
            output_label.delete(1.0, END)
            count = 0
            #output_label.delete('1.0', END)
            for i in range(len(cityOption)):
                if(tkVarForFileLoop[i].get()==1):
                    count=i

            output_label.insert(END, cityOption[count]+" added\n")
            citySelected.append(cityOption[count])
            output_label.insert(END, "\n\n")
            output_label.insert(END, "Current list:\n")
            for i in range(len(citySelected)):
                output_label.insert(END, citySelected[i]+"\n")
            output_label.insert(END, str(len(citySelected)))


            #if (city2.get() == 1):
            #    global PittsHolder
            #    PittsHolder = 'Pittsburgh'
            #    output_label.insert(END, PittsHolder+" added\n")
            #    output_label.insert(END, "\n")



        # def compound_label(self):
        #     source_label.config(text="Use a combination of historic data and user data to train the model.")
        #     #blocks out dropdown
        #     label = Label(text="            ", bg="#525453")
        #     label.place(relx=.05, rely=.3, relwidth=.33, relheight=.25)

        def run_train(self):

            a = HistAccess()
            num_cities = (len(citySelected))

            flag = False
            while True:
                if start_year_parameter.get() == "not selected" or end_year_parameter.get() == "not selected":
                    messagebox.showinfo("System Message", "Please select a start year and end year")
                    break
                elif num_cities < 4:
                    messagebox.showinfo("System Message", "Please Select 4 cites from the list")
                    # training_label = Label(upperframe, text="!System Message! - Please Select 4 cites from the list", font="100", bg='#525453',
                    #                    fg='white')
                    # training_label.place(relx=.3, rely=.9)
                    break
                elif future_time_parameter.get() == "not selected":
                    messagebox.showinfo("System Message", "Please select a future time")
                    break
                else:
                    messagebox.showinfo("System Message", "Training is currently in progress...")
                    # training_label = Label(upperframe, text="!System Message! - Training is currently in progress.....", font="100", bg='#525453',
                    #                        fg='white')
                    # training_label.place(relx=.3, rely=.9)
                    flag = True
                    break
            # output_label.insert(tkinter.END,"Before getData connection\n\n")
            output_label.delete("1.0", END)
            output_label.insert(END, "Number of cities selected:" + str(len(citySelected)))

            # a.getData(citySelected, int(start_year_parameter.get()), int(end_year_parameter.get()))
            if flag:
                a.getData(num_cities, citySelected, int(start_year_parameter.get()), int(end_year_parameter.get()))
                test = RNN.RNN
                out = test.runRNN(test, int(future_time_parameter.get()))
                citySelected.clear()
                output_label.delete("1.0", END)
                output_label.insert(END, "Output:" + out)

        # Train Interface Events
        def saveSelection(lb):
            selection = []
            for i in lb.curselection():
                selection.append(lb.get(i))
            return selection

        def restoreSelection(lb, selectedItems):
            lb.selection_clear(0, "end")
            items = lb.get(0, "end")
            for item in selectedItems:
                if item in items:
                    index = items.index(item)
                    lb.selection_set(index)

        # global selectedITem
        def onselect(evt):
            # Note here that Tkinter passes an event object to onselect()

            output_label.delete('1.0', END)
            w = evt.widget
            x = 0
            index = int(w.curselection()[0])
            value = w.get(index)
            # selectedItem.append(index, value)

            output_label.insert(END, 'You selected: "%s"\n\n' % (value))
            global citySelected
            citySelected.append(value)
            citySelected = list(dict.fromkeys(citySelected))
            output_label.insert(END, 'Current selected cities:"\n\n')

            for i in range(len(citySelected)):
                output_label.insert(END, str(citySelected[i]) + "\n")
            output_label.insert(END, str(len(citySelected)))
            restoreSelection(surrounding_cities_listbox, citySelected)

    # Surrounding Cities ListBox
        surrounding_cities_listbox = Listbox(upperframe, exportselection=False)
        surrounding_cities_listbox.place(relx=.4, rely=.1, relwidth=.2, relheight=.2)

        global enable
        enable = []
        for i in range(len(cityOption)):
            enable.append(i)


        for item in cityOption:
            surrounding_cities_listbox.insert(END, item)
            for y in enable:
                globals()["var{}{}".format(item, y)] = BooleanVar()
                globals()["checkbox{}{}".format(item, y)] = Checkbutton(upperframe, text=y,
                                                                        variable=globals()["var{}{}".format(item, y)])
        saveSelection(surrounding_cities_listbox)

        surrounding_cities_listbox.bind('<<ListboxSelect>>', onselect)


    # Target Cities Listbox
        target_cities_listbox = Listbox(upperframe, exportselection=False)
        target_cities_listbox.place(relx=.7, rely=.1, relwidth=.2, relheight=.2)

        for i in range(len(targetCityOption)):
            enable.append(i)


        for item in targetCityOption:
            target_cities_listbox.insert(END, item)
            for y in enable:
                globals()["var{}{}".format(item, y)] = BooleanVar()
                globals()["checkbox{}{}".format(item, y)] = Checkbutton(upperframe, text=y,
                                                                        variable=globals()["var{}{}".format(item, y)])
        target_cities_listbox.bind('<<ListboxSelect>>', onselect)

    entry_values = []
    # load items for Testing page
    def init_Test(self):
        # self.indexNav.cofig(state=NORMAL)
        # self.trainNav.config(state=NORMAL)
        # self.testNav.config(state=DISABLED)
        # self.CityOptionNav.config(state=NORMAL)
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
        # title = Label(upperframe, text="Test", bg='#525453', font=100)
        # title.place(relx=.5, rely=.02)
        source_label = Label(upperframe, bg='#525453', fg='white')
        source_label.place(relx=0.05, rely=.2)
        input_label = Label(upperframe, text="Choose Input Source:", bg='#525453', fg='white', font=100)
        input_label.place(relx=0, rely=.02, relwidth=.2, relheight=.1)
        str_out = StringVar()

        cover_box = Frame(root, bg='#525453', highlightcolor='#525453')
        cover_box.place(relx=.35, rely=.1, relwidth=.6, relheight=.3)

        input_label = Label(upperframe, text="Choose surrounding cities from the list:", fg="white", bg='#525453',
                            font=100)
        input_label.place(relx=.37, rely=.02, relwidth=.3, relheight=.1)

        input_label2 = Label(upperframe, text="Choose a target city from the list:", fg="white", bg='#525453',
                             font=100)
        input_label2.place(relx=.65, rely=.02, relwidth=.3, relheight=.1)

        entry_button = Button(upperframe, text="Enter Data", fg="black", bg="white", font=100, command=lambda: open_manual_entry(self))
        #hr
        divide_label = Label(upperframe,
                             text=".....................................................................................................................................................................................................................................................................",
                             fg="white", bg='#525453',
                             font=100)
        divide_label.place(relx=-.0, rely=0.5)
        #output
        output_title = Label(upperframe, text="Output: ", bg='#525453', fg='white', font=100)
        output_title.place(relx=.5, rely=.55, relwidth=.1, relheight=.1)
        output_label = tkinter.Text(upperframe, height=2, width=30)
        output_label.place(relx=.5, rely=.65, relwidth=.4, relheight=.2)
        # make buttons
        v = StringVar()
        current_button = Radiobutton(upperframe, text="Current", variable=v, value="current", borderwidth=5,
                                     bg='#525453', fg='white', command=lambda: current_label(self))
        current_button.place(relx=.05, rely=.1)
        manual_button = Radiobutton(upperframe, text="Manual", variable=v, value="manual", borderwidth=5, bg='#525453',
                                    fg='white', command=lambda: manual_label(self))
        manual_button.place(relx=.15, rely=.1)


        run_label = Label(upperframe, text="Press the button below to begin generate a predicion", font="100", bg='#525453',
                          fg='white')
        run_label.place(relx=.05, rely=.57)
        run_button = Button(upperframe, text="Run", borderwidth=5, bg='white', fg='black',
                            command=lambda: run_test(self), state=DISABLED)
        run_button.place(relx=0.165, rely=.7, relwidth=.1, relheight=.1)

        def current_label(self):
            source_label.config(text="Use current data to make a prediction.")
            self.current = True  # set boolean to true to let controller know to use current data later
            run_button.config(state=NORMAL)
            surrounding_cities_listbox.config(state=DISABLED)
            target_cities_listbox.config(state=DISABLED)
            entry_button.config(state=DISABLED)

        def fetch(entries):
            counter = 0
            for entry in entries:
                field = entry[0]
                text = entry[1].get()
                print(text)
                num = int(text)
                out = (((num - 32) * 5/9) + 273.15)
                self.entry_values.append(out)
                counter += 1
            return

        def make_form(root, fields):
            entries = []
            for field in fields:
                row = Frame(root)
                lab = Label(row, width=15, text=field, anchor='w')
                ent = Entry(row)
                row.pack(side=TOP, fill=X, padx=5, pady=5)
                lab.pack(side=LEFT)
                ent.pack(side=RIGHT, expand=YES, fill=X)
                entries.append((field, ent))
            return entries


        def manual_label(self):
            source_label.config(text="Use manually inputted data to make a prediction.")
            self.current = False  # set boolean to false to know to use manually inputted data
            run_button.config(state=NORMAL)
            cover_box.destroy()
            surrounding_cities_listbox.config(state=NORMAL)
            target_cities_listbox.config(state=NORMAL)
            entry_button.config(state=NORMAL)
            entry_button.place(relx=0.05, rely=.3)

        # Test Interface Events
        def saveSelection(lb):
            selection = []
            for i in lb.curselection():
                selection.append(lb.get(i))
            return selection

        def restoreSelection(lb, selectedItems):
            lb.selection_clear(0, "end")
            items = lb.get(0, "end")
            for item in selectedItems:
                if item in items:
                    index = items.index(item)
                    lb.selection_set(index)

        # global selectedITem
        def onselect(evt):
            # Note here that Tkinter passes an event object to onselect()

            output_label.delete('1.0', END)
            w = evt.widget
            x = 0
            index = int(w.curselection()[0])
            value = w.get(index)
            # selectedItem.append(index, value)

            output_label.insert(END, 'You selected: "%s"\n\n' % (value))
            global testCitySelected
            testCitySelected.append(value)
            testCitySelected = list(dict.fromkeys(testCitySelected))
            output_label.insert(END, 'Current selected cities:"\n\n')

            for i in range(len(testCitySelected)):
                output_label.insert(END, str(testCitySelected[i]) + "\n")
            output_label.insert(END, str(len(testCitySelected)))
            restoreSelection(surrounding_cities_listbox, testCitySelected)

        # Surrounding Cities ListBox
        surrounding_cities_listbox = Listbox(upperframe, exportselection=False)
        surrounding_cities_listbox.place(relx=.4, rely=.1, relwidth=.2, relheight=.2)

        global enable
        enable = []
        for i in range(len(cityOption)):
            enable.append(i)

        for item in cityOption:
            surrounding_cities_listbox.insert(END, item)
            for y in enable:
                globals()["var{}{}".format(item, y)] = BooleanVar()
                globals()["checkbox{}{}".format(item, y)] = Checkbutton(upperframe, text=y,
                                                                        variable=globals()[
                                                                            "var{}{}".format(item, y)])
        saveSelection(surrounding_cities_listbox)

        surrounding_cities_listbox.bind('<<ListboxSelect>>', onselect)

        # Target Cities Listbox
        target_cities_listbox = Listbox(upperframe, exportselection=False)
        target_cities_listbox.place(relx=.7, rely=.1, relwidth=.2, relheight=.2)

        for i in range(len(targetCityOption)):
            enable.append(i)

        for item in targetCityOption:
            target_cities_listbox.insert(END, item)
            for y in enable:
                globals()["var{}{}".format(item, y)] = BooleanVar()
                globals()["checkbox{}{}".format(item, y)] = Checkbutton(upperframe, text=y,
                                                                        variable=globals()[
                                                                            "var{}{}".format(item, y)])
        target_cities_listbox.bind('<<ListboxSelect>>', onselect)

        def open_manual_entry(self):
            root = Tk()
            ents = make_form(root, testCitySelected)
            b1 = Button(root, text='Confirm',
                  command=(lambda e=ents: fetch(e)))
            b1.pack(side=BOTTOM, padx=5, pady=5)


            # root.mainloop()

            # city1_label = Label(upperframe, text=citySelected[0]).grid(row=0)
            # city2_label = Label(upperframe, text=citySelected[1]).grid(row=1)
            # city3_label = Label(upperframe, text=citySelected[2]).grid(row=2)
            #
            # e1 = Entry(upperframe)
            # e2 = Entry(upperframe)
            # e3 = Entry(upperframe)
            #
            # e1.grid(row=0, column=1)
            # e2.grid(row=1, column=1)
            # e3.grid(row=2, column=1)

        def run_test(self):

            model = load_model("/Users/Tigergoodbread/PycharmProjects/AI-Forecast/model-50.hdf5")
            test = np.zeros((1, 1, 3))

            if self.current == True:
                api_access = APIAccess.APIAccess
                api_access.getCurrent(api_access)
                test[0][0][0] = (api_access.temp_1 - 244) / (323 - 244)
                test[0][0][1] = (api_access.temp_2 - 244) / (323 - 244)
                test[0][0][2] = (api_access.temp_3 - 244) / (323 - 244)
                current_temp = api_access.temp

            else:
                while True:
                    if len(testCitySelected) < 4:
                        messagebox.showinfo("System Message", "Please Select 4 cites from the list")
                        # training_label = Label(upperframe, text="!System Message! - Please Select 4 cites from the list", font="100", bg='#525453',
                        #                    fg='white')
                        # training_label.place(relx=.3, rely=.9)
                        break
                    else:
                        # messagebox.showinfo("System Message", "A prediction is being generated...")
                        # training_label = Label(upperframe, text="!System Message! - Training is currently in progress.....", font="100", bg='#525453',
                        #                        fg='white')
                        # training_label.place(relx=.3, rely=.9)
                        break
                test[0][0][0] = (self.entry_values[0] - 244) / (323 - 244)
                test[0][0][1] = (self.entry_values[1] - 244) / (323 - 244)
                test[0][0][2] = (self.entry_values[2] - 244) / (323 - 244)
                current_temp = self.entry_values[3]


            prediction = model.predict(test)
            str_out.set("Current Temp: " + str((current_temp - 273.15) * (
                        9 / 5) + 32) + "\nPredicted Temp " + future_time_parameter.get() + " hours from now: "
                        + str(((prediction[0][0] * (323.0 - 244.0) + 244.0) - 273.15) * (9.0 / 5.0) + 32.0))

            output_label.delete('1.0', END)
            output_label.insert(tkinter.END, str_out.get())

#=====================================================================================================================
    def client_exit(self):
        exit()

    def user_input(self):
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


        intro_label = Label(upperframe, text="Now, finish the input box to create your own data object:", fg="pink", bg='#525453',font=200)
        intro_label.pack()

        cont = BooleanVar()
        cont.set(True)

        #
        global cityHolder
        #
        global yearHolder
        global monthHolder
        global dayHolder
        global hourHolder
        global tempHolder
        global temp_minHolder
        global temp_maxHolder
        global pressureHolder
        global humidityHolder
        global wind_speedHolder
        global wind_dirHolder

        while cont.get() == True:
            cont.set(False)
            ############Enter City ###################
            USER_INP0 = simpledialog.askstring(title="Step0", prompt="Please enter City:")
            ##########################################
            USER_INP1 = simpledialog.askstring(title="Step1", prompt="Please enter year:")
            USER_INP2 = simpledialog.askstring(title="Step2", prompt="Please enter Month:")
            USER_INP3 = simpledialog.askstring(title="Step3", prompt="Please enter Day:")
            USER_INP4 = simpledialog.askstring(title="Step4", prompt="Please enter Hour:")
            USER_INP5 = simpledialog.askstring(title="Step5", prompt="Please enter Temp:")
            USER_INP6 = simpledialog.askstring(title="Step6", prompt="Please enter Minimum Temp:")
            USER_INP7 = simpledialog.askstring(title="Step7", prompt="Please enter Maximum Temp:")
            USER_INP8 = simpledialog.askstring(title="Step8", prompt="Please enter Pressure:")
            USER_INP9 = simpledialog.askstring(title="Step9", prompt="Please enter Humidity:")
            USER_INP10 = simpledialog.askstring(title="Step10", prompt="Please enter Wind Speed:")
            USER_INP11 = simpledialog.askstring(title="Step11", prompt="Please enter Wind Direction:")

            #
            cityHolder = USER_INP0
            #
            yearHolder = USER_INP1
            monthHolder = USER_INP2
            dayHolder = USER_INP3
            hourHolder = USER_INP4
            tempHolder = USER_INP5
            temp_minHolder = USER_INP6
            temp_maxHolder = USER_INP7
            pressureHolder = USER_INP8
            humidityHolder = USER_INP9
            wind_speedHolder = USER_INP10
            wind_dirHolder = USER_INP11

            USER_INP12 = simpledialog.askstring(title="Continue?", prompt="Do you want to input another piece of data? (y/Y for yes)")

            if(USER_INP12 == "y" or USER_INP12 =="Y"):
                cont.set(True)
        #
        testOutput0 = Label(upperframe, text=USER_INP0, bg='#525453')
        testOutput0.place(relx=0, rely=.1, relwidth=1, relheight=.03)
        #
        testOutput1 = Label(upperframe, text=USER_INP1, bg='#525453')
        testOutput1.place(relx=0, rely=.1, relwidth=1, relheight=.03)
        testOutput2 = Label(upperframe, text=USER_INP2, bg='#525453')
        testOutput2.place(relx=0, rely=.12, relwidth=1, relheight=.02)
        testOutput3 = Label(upperframe, text=USER_INP3, bg='#525453')
        testOutput3.place(relx=0, rely=.14, relwidth=1, relheight=.02)
        testOutput4 = Label(upperframe, text=USER_INP4, bg='#525453')
        testOutput4.place(relx=0, rely=.16, relwidth=1, relheight=.02)
        testOutput5 = Label(upperframe, text=USER_INP5, bg='#525453')
        testOutput5.place(relx=0, rely=.18, relwidth=1, relheight=.02)
        testOutput6 = Label(upperframe, text=USER_INP6, bg='#525453')
        testOutput6.place(relx=0, rely=.20, relwidth=1, relheight=.02)
        testOutput7 = Label(upperframe, text=USER_INP7, bg='#525453')
        testOutput7.place(relx=0, rely=.22, relwidth=1, relheight=.02)
        testOutput8 = Label(upperframe, text=USER_INP8, bg='#525453')
        testOutput8.place(relx=0, rely=.24, relwidth=1, relheight=.02)
        testOutput9 = Label(upperframe, text=USER_INP9, bg='#525453')
        testOutput9.place(relx=0, rely=.26, relwidth=1, relheight=.02)
        testOutput10 = Label(upperframe, text=USER_INP10, bg='#525453')
        testOutput10.place(relx=0, rely=.28, relwidth=1, relheight=.02)
        testOutput11 = Label(upperframe, text=USER_INP11, bg='#525453')
        testOutput11.place(relx=0, rely=.30, relwidth=1, relheight=.02)
        testOutput12 = Label(upperframe, text=USER_INP12, bg='#525453')
        testOutput12.place(relx=0, rely=.32, relwidth=1, relheight=.02)

    def expand_Options(self):
        # self.indexNav.cofig(state=NORMAL)
        # self.trainNav.config(state=NORMAL)
        # self.testNav.config(state=NORMAL)
        # self.CityOptionNav.config(state=NORMAL)
        # changing the title of our master widget
        self.master.title("City Edit Menu")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # make canvas
        canvas = Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()
        # make frames
        upperframe = Frame(root, bg='#525453')
        upperframe.place(relx=0, rely=.05, relwidth=1, relheight=.95)

        intro_label = Label(upperframe, text="Edit the surroundings city options testing and training using the options below:", fg="pink",bg='#525453', font=200)
        intro_label.pack()

        b = Button(upperframe, text="Clear City Options", command=lambda:deleteCityOption(self))
        b.pack()
        c = Button(upperframe, text="Add a new city the the list", command=lambda: addCityOption(self))
        c.pack()
        d = Button(upperframe, text="Update", command=lambda: file_prep(self))
        d.pack()
        #USER_INP0 = simpledialog.askstring(title="Erase?",prompt="Do you want to erase previous option contents? ")
        #if(USER_INP0=='Y' or USER_INP0=='y'):
        #    cityOption.clear()
        #    f= open("AllCityName.txt", "wb")
        #    f.close()
        #    alert_popup("Receipt", "The option panel is empty now!", "-----------------------")
        #else:
            #USER_INP1 = simpledialog.askstring(title="Update", prompt="Please enter the City name you want to add to the list:")#

            #f = open("AllCityName.txt", "a+")
            #f.write(USER_INP1+",")
            #f.close()
            #alert_popup("Receipt", "Your city has been added into the option!", "----------------------")

            #f = open("AllCityName.txt","a")
            #f.write(USER_INP1)
            #f.close()

        def load_in_CityOption(self):
            alert_popup("Receipt", "Action!")

        def addCityOption(self):
            USER_INP1 = simpledialog.askstring(title="Update",prompt="Please enter the City name you want to add to the list:")  #

            f = open("AllCityName.txt", "a+")
            f.write(USER_INP1 + ",")
            f.close()
            alert_popup("Receipt", "Your city has been added into the option!", "----------------------")

        def deleteCityOption(self):
            open('AllCityName.txt', 'w').close()
            cityOption.clear()
            alert_popup("Receipt", "The option panel is empty now!", "-----------------------")

        def file_prep(self):
        #alert_popup("test", "test!", "----------------------")
            global cityCount
            global cityOption
        #i = IntVar()
        #i = 0

            with open("AllCityName.txt") as f:
                for item in f:
                    for i in item.split(","):
                        cityOption.append(i)
                        #i+=1
            #cityCount = str(i)
            if(len(cityOption)!=0):
                cityOption.pop()
            cityOption2=list(dict.fromkeys(cityOption))

            cityOption = cityOption2

            alert_popup("success", "Your city options list have been refreshed!", "Return to the Train or Test menu to see your changes.")
            f.close()

            open('file.txt', 'w').close()







###########################################################################################

############################################################################
root = Tk()

variable = StringVar()
root.geometry("1000x600")
app = Window(root)
root.mainloop()
