import tkinter
from tkinter import *
from tkinter import simpledialog

from DataAccess import APIAccess
########    add   #################
from DataAccess import HistAccess
from DataAccess.HistAccess import HistAccess
from Examples import RNN
from DataAccess.load_data import load_data_class
# from DataAccess.CopyOfWorkingRNN import kerasBatch

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
cityOption = ['Buffalo', 'Cleveland', 'Pittsburgh', 'Erie']
citySelected = []
##############    for city option looping   ######################
tkVarForFileLoop = []
################################################################


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
   b = Button(root, text="<Continue>", command=root.destroy, width=10)
   b.pack()
   mainloop()
#########################################################################################################
alert_popup("!!!Welcome!!!!", "Senior Design Project:\nAI Wether Forcast", "Team #11")
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

       ##########################                      add                    ##############################
       # exitNav = Button(nav, text="Exit", borderwidth=5, bg='#525453', fg='#d4d5d6', command=self.client_exit)
       # exitNav.place(relx=.8, rely=0, relwidth=.1, relheight=1)
       # userInputNav = Button(nav, text="Create Data", borderwidth=5, bg='#525453', fg='#d4d5d6',command=self.user_input)
       # userInputNav.place(relx=.3, rely=0, relwidth=.1, relheight=1)
       CityOptionNav = Button(nav, text="CityOptions", borderwidth=5, bg='#525453', fg='#d4d5d6', command=self.expand_Options)
       CityOptionNav.place(relx=.4, rely=0, relwidth=.1, relheight=1)

       #############################################            Test            #######################################
       # TTNav = Button(nav, text="test_test", borderwidth=5, bg='#525453', fg='#d4d5d6', command=self.test_test)
       # TTNav.place(relx=.7, rely=0, relwidth=.1, relheight=1)

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
       #output_label = Label(upperframe,text="                        ", bg='#525453', font=100)
       #output_label.place(relx=.5, rely=.2, relwidth=.2, relheight=.2)

########################            Surrounding Cities GUI          ######################################

       input_label = Label(upperframe, text="Choose surrounding cities from the list:", fg="pink", bg='#525453',
                           font=100)
       input_label.place(relx=.05, rely=0.3, relwidth=.4, relheight=.3)


       #listbox = Listbox(upperframe)
       #listbox.place(relx=0.07, rely=.5)
       ###########################          two different things      ##############################
       #city1 = tkinter.IntVar()
       #city2 = tkinter.IntVar()
       #city3 = tkinter.IntVar()
       #c1 = tkinter.Checkbutton(upperframe, text='Buffalo', variable=city1, onvalue=1, offvalue=0,
       #                         command=lambda: confirm_selection(self))
       #c1.place(relx=.05, rely=0.5)
       #c2 = tkinter.Checkbutton(upperframe, text='Pittsburgh', variable=city2, onvalue=1, offvalue=0,
       #                         command=lambda: confirm_selection(self))
       #c2.place(relx=.05, rely=0.6)
       #c3 = tkinter.Checkbutton(upperframe, text='Cleveland', variable=city3, onvalue=1, offvalue=0,
       #                         command=lambda: confirm_selection(self))
       #c3.place(relx=.05, rely=0.7)


       #for machine in enable:
       #    enable[machine] = Variable()
       #    l = Checkbutton(self.root, text=machine, variable=enable[machine])
       #    l.pack()

       for i in range(len(cityOption)):
           tkVarForFileLoop.append(IntVar())

       for k in range(len(cityOption)):
           l = tkinter.Checkbutton(upperframe, text=cityOption[k], variable=tkVarForFileLoop[k], onvalue=1, offvalue=0, command=lambda: confirm_selection(self))
           l.place(relx=.05, rely=.8)



       #output_label = tkinter.Text(upperframe, height=2, width=30)
       #output_label.place(relx=.5, rely=0.5, relwidth=.4, relheight=.3)

       #############Ouput Receipt##############
       output_title = Label(upperframe, text="Receipt:", bg='#525453', font=100)
       output_title.place(relx=.45, rely=.07, relwidth=.2, relheight=.2)
       output_label = tkinter.Text(upperframe, height=2, width=30)
       output_label.place(relx=.5, rely=.2, relwidth=.2, relheight=.2)

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

   ####################################                  Functionality                ######################################################
       def historic_label(self):
           source_label.config(text="Use historic data to train the model.")
           years_label = Label(text="Select starting and ending year of weather Data::", bg='#525453', fg="white")
           years_label.place(relx=.05, rely=.3)
           variable1 = StringVar(upperframe)
           variable2 = StringVar(upperframe)

           variable1.set("not selected")  # default value
           variable2.set("not selected")  # default value
           start_year = OptionMenu(root, variable1, "2001", "2002", "2003", "2004", "2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019")
           start_year.place(relx=.05, rely=.35)
           end_year = OptionMenu(root, variable2, "2001", "2002", "2003", "2004", "2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019")
           end_year.place(relx=.15, rely=.35)

           global start_year_parameter
           start_year_parameter = variable1
           global end_year_parameter
           end_year_parameter = variable2


       def user_label(self):
           source_label.config(text="Use user data to train the model.")
           #blocks out dropdown
           label = Label(text="            ", bg="#525453")
           label.place(relx=.05, rely=.3, relwidth=.03, relheight=.02)

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
           #output_label.insert(tkinter.END,"Before getData connection\n\n")
           output_label.insert(END, "citySelected:" + str(len(citySelected)))

           # a.getData(citySelected, int(start_year_parameter.get()), int(end_year_parameter.get()))
           a.getData(num_cities, citySelected, int(start_year_parameter.get()), int(end_year_parameter.get()))
           test = RNN.RNN
           test.runRNN(test)

       def onselect(evt):
           # Note here that Tkinter passes an event object to onselect()
           output_label.delete('1.0', END)
           w = evt.widget
           x = 0
           index = int(w.curselection()[0])
           value = w.get(index)
           output_label.insert(END, 'You selected City %d: "%s"\n\n' % (index, value))
           global citySelected
           citySelected.append(value)
           citySelected = list(dict.fromkeys(citySelected))
           output_label.insert(END, 'Current selected city:"\n\n')

           for i in range(len(citySelected)):
               output_label.insert(END, str(citySelected[i]) + "\n")
           output_label.insert(END, str(len(citySelected)))

       listbox = Listbox(upperframe)
       listbox.place(x=3, y=100)

       global enable
       enable = []
       for i in range(len(cityOption)):
           enable.append(i)


       for item in cityOption:
           listbox.insert(END, item)
           for y in enable:
               globals()["var{}{}".format(item, y)] = BooleanVar()
               globals()["checkbox{}{}".format(item, y)] = Checkbutton(upperframe, text=y,
                                                                       variable=globals()["var{}{}".format(item, y)])

       listbox.bind('<<ListboxSelect>>', onselect)



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
       output_label.place(relx=.45, rely=.2, relwidth=.2, relheight=.1)
       #make buttons
       v = StringVar()
       current_button = Radiobutton(upperframe, text="Current", variable=v, value="current", borderwidth=5, bg='#525453', fg='black', command=lambda: current_label(self))
       current_button.place(relx=.05, rely=.1)
       manual_button = Radiobutton(upperframe, text="Manual", variable=v, value="manual", borderwidth=5, bg='#525453', fg='black', command=lambda: manual_label(self))
       manual_button.place(relx=.15, rely=.1)
       #Could use polymorphism
       run_button = Button(upperframe, text="RunCurrent", borderwidth=5, bg='#525453', fg='#d4d5d6', command=lambda: run_test(self))
       run_button.place(relx=.75, rely=.1)
       run_button = Button(upperframe, text="RunManual", borderwidth=5, bg='#525453', fg='#d4d5d6',command=lambda: run_test2(self))
       run_button.place(relx=.75, rely=.2)

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

           #str_out.set("Year, Month, Day, Hour, Temp, Min Temp, Max Temp, Humidity, Pressure, Wind Speed, Wind Direction" + "\n" + str_erie + "\n" + str_city1 + "\n" + str_city2 + "\n" + str_city3)
           output_label = tkinter.Text(upperframe, height=2, width=30)
           output_label.place(relx=.5, rely=.2, relwidth=.2, relheight=.2)
           output_label.insert(tkinter.END, "Year, Month, Day, Hour, Temp, Min Temp, Max Temp, Humidity, Pressure, Wind Speed, Wind Direction" + "\n" + str_erie + "\n" + str_city1 + "\n" + str_city2 + "\n" + str_city3)

           label = Label(text="Using the testing data listed above, Here is our prediction result:", bg="#525453")
           label.place(relx=-.02, rely=.5, relwidth=.5, relheight=.1)
           output_label = tkinter.Text(upperframe, height=2, width=30)
           output_label.place(relx=.5, rely=.6, relwidth=.2, relheight=.2)
           #output_label.insert(tkinter.END)

       def run_test2(self):

           label = Label(text="These are the data you just created:", bg="#525453")
           label.place(relx=.02, rely=.4, relwidth=.5, relheight=.1)

           output_label = tkinter.Text(upperframe, height=2, width=30)
           output_label.insert(tkinter.END, "In case that you have not build up your data, go to \"create\" and do so")
           output_label.place(relx=.5, rely=.6, relwidth=.2, relheight=.2)

           global frameWord
           frameWord = "City, Year, Month, Day, Hour, Temp, MinTemp, MaxTemp, Humidity, Pressure, Wind Speed, Wind Direction"
           global content
           content = "\n" + cityHolder + ": " + yearHolder + ", " + monthHolder+ ", " + dayHolder + ", " + hourHolder + ", " +tempHolder+ ", " + temp_minHolder + ", " +temp_maxHolder+ ", " + pressureHolder+ ", " +humidityHolder+ ", " + wind_speedHolder + ", " + wind_dirHolder

           output_label.delete('1.0', END)
           output_label.insert(tkinter.END, frameWord + content)

           #Year, Month, Day, Hour, Temp, Min
           #Temp, Max
           #Temp, Humidity, Pressure, Wind
           #Speed, Wind
           #Direction
           #Erie: 2020, 3, 18, 23, 278.72, 277.15, 280.37, 93, 1019, 5.87, 114

           #label2 = Label(text="In case that you have not build up your data, go to \"create\" and do so", bg="#525453")
           #label2.place(relx=-.02, rely=.5, relwidth=.5, relheight=.1)

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

       intro_label = Label(upperframe, text="Here we can expand more city options :", fg="pink",bg='#525453', font=200)
       intro_label.pack()

       b = Button(upperframe, text="Delete previous city list", command = lambda:deleteCityOption(self))
       b.pack()
       c = Button(upperframe, text="Add a new city to the list", command=lambda: addCityOption(self))
       c.pack()
       d = Button(upperframe, text="Load newly added ones", command=lambda: file_prep(self))
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

           alert_popup("success", "All the city names are added to the list for you selection!", "-_-")
           f.close()

           open('file.txt', 'w').close()


#################################################################################################################################
   def test_test(self):
       # changing the title of our master widget
       self.master.title("Train Menu")

       # allowing the widget to take the full space of the root window
       self.pack(fill=BOTH, expand=1)
       # make canvas
       canvas = Canvas(root, height=HEIGHT, width=WIDTH)
       canvas2 = Canvas(root, height=2000, width=2000)
       #canvas = Canvas(root, height=2000, width=2000)
       canvas.pack()
       canvas2.pack()
       # make frames
       upperframe = Frame(root, bg='#525453')
       upperframe.place(relx=0, rely=.05, relwidth=1, relheight=.95)


##################             Test thing out here             #####################################################################################33





###########################################################################################

############################################################################
root = Tk()

variable = StringVar()
root.geometry("1000x600")
app = Window(root)
root.mainloop()

