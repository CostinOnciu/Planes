from tkinter import * 
from Entities import ButtonForRepo
from Erros import RepoError, RandomPlaneError
from _functools import partial

class GUI(object):
    def __init__(self, service):  
        self.__service = service
    
    def InitializeTables(self,frame):
        self.__service.InitializeTable("gui","grey","NAI",frame,0)
        self.__service.InitializeTable("gui","white","AI",frame,30)
        self.__service.RandomizeAiPlanes("gui",frame)

    def reset(self,*frame):
        self.__service.Reset("gui",frame[0])
    
    def start(self):
        master = Tk() 
        master.title('Airplanes')
        master.geometry('1000x1000+400+100')
        
        frame = Frame(master)
        frame.pack(fill=X)
        
        event = partial(self.reset,frame)
        button = Button(master, text = "Reset game",command = event)
        button.pack(fill = X)
        
        try :
            self.InitializeTables(frame)
        except RandomPlaneError:
            self.InitializeTables(frame)
        
        mainloop()

class UI(object):
    def __init__(self,service):
        self.__service = service
    
    def InitializeTables(self):
        self.__service.InitializeTable("ui","grey","NAI")
        self.__service.InitializeTable("ui","white","AI")
        self.__service.RandomizeAiPlanes("ui")
        
    def PrintTables(self):
        PlayerTable = self.__service.GetPlayerTable()
        AiTable = self.__service.GetAiTable()
    
        for i in PlayerTable:
            for j in i:
                print(j, end='')
            print(" ")
        print(" ")   
        for i in AiTable:
            for j in i:
                print(j, end='')
            print(" ")
        print(" ")
        
    def add_plane(self):
        position = input("Give the position of the cockpit ")
        if len(position) != 2:
            print("Please insert a valid position")
            return
        #try :
        decoder = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8}
        row = position[0]
        try:
            row = decoder[row.upper()]
        except KeyError:
            print("Invalid value")
            return
        try:
            column = int(position[1])
        except ValueError:
            print("Invalid value")
            return
        
        try:
            self.__service.AddPlayerPlane(row-1,column-1,"ui","blue","NAI")
        except RepoError as error:
            print(error)

    def attack(self):
        position = input("Give the position u want to attack ")
        if len(position) != 2:
            print("Please insert a valid position")
            return
        #try :
        decoder = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8}
        row = position[0]
        try:
            row = decoder[row.upper()]
        except KeyError:
            print("Invalid value")
            return
        try:
            column = int(position[1])
        except ValueError:
            print("Invalid value")
            return
        
        returned_value = self.__service.HitAi(row-1,column-1)
        if returned_value != None:
            return returned_value
        
        
    def reset(self):
        self.__service.Reset("ui")
    
    def start(self):
        commands = {"1":self.add_plane,
                    "2":self.reset,
                    "3":self.attack}
        try:
            self.InitializeTables()
        except RandomPlaneError:
                pass
        while True:
            command = input("enter command : ")
            if command in commands:
                returned_value = commands[command]()
                if returned_value == None:
                    self.PrintTables()
                elif returned_value == -1:
                        print("You lost! ")
                        return
                else:
                        print("You won! ")
                        return
            elif command == "x":
                return
            else:
                print("Enter a valid command!")
            