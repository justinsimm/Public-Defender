import tkinter as tk
import customtkinter
from tkinter import ttk
 

LARGEFONT =("Verdana", 35)

class tkinterApp(customtkinter.Ctk):
    
    def __init__(self, *args, **kwargs): 
        super().__init__(self)
        #Configure window
        self.configure()
        self.minsize(200, 200)
        self.maxsize(500, 500)
        self.geometry("300x300+200+200")

        #Tab View
        self.tab_view = customtkinter.CTkTabview(master=self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_view.add("Risk Analysis")
        self.tab_view.add("Recommendations") 
 
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
 
            frame = F(container, self)
 
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
 
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)
        

        self.show_frame(StartPage)
 
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class getStartPage(controller.show_frame(StartPage)):


# Risk Analysis Page
class StartPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        button1 = ttk.Button(self, text ="Risk Analysis",
            command = lambda : controller.show_frame(Page1))
        button1.grid(row = 0, column = 0, padx = 0, pady = 0)

        ## button to show frame 2 with text layout2
        button2 = ttk.Button(self, text ="Page 2",
        command = lambda : controller.show_frame(Page2))
    
        # putting the button in its place by
        # using grid
        button2.grid(row = 0, column = 1, padx = 0, pady = 0)

         
 
 
#Recommendations Page
class Page1(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
 
        #Navbar
        button1 = ttk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(StartPage))
        button1.grid(row = 0, column = 0, padx = 0, pady = 0)
 
        button2 = ttk.Button(self, text ="Page 2",
                            command = lambda : controller.show_frame(Page2))
        button2.grid(row = 0, column = 1, padx = 0, pady = 0)
 
 
 
 
# third window frame page2
class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #Navbar
        button1 = ttk.Button(self, text ="Page 1",
                            command = lambda : controller.show_frame(Page1))
        button1.grid(row = 0, column = 1, padx = 0, pady = 0)
 
    
        button2 = ttk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))
        button2.grid(row = 0, column = 0, padx = 0, pady = 0)
 
 
# Driver Code
app = tkinterApp()
app.mainloop()

