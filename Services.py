from Entities import ButtonForRepo
import random
import copy
from tkinter import *
from _functools import partial
from Erros import RepoError

class ServiceGame(object):
    def __init__(self,player_table,ai_table):
        self.__player_table = player_table
        self.__ai_table = ai_table
        self.__choice = [[2,0],[2,1],[2,2],[2,3],[2,4],
                         [3,0],[3,1],      [3,3],[3,4],
                         [4,0],[4,1],      [4,3],[4,4],
                         [5,0],[5,1],[5,2],[5,3],[5,4]]
        self.__thinking_choice = []
        self.__ai_planes_down = 0
        self.__player_planes_down = 0
    
    def GetPlayerTable(self):
        return self.__player_table.get_all()
    
    def GetAiTable(self):
        return self.__ai_table.get_all()

    def NotPlane(self,*args):
        '''
        :cell = args[0][0] it's an entity
            it's the event that triggers when the AI choses a position on the player table and it's not a plane
        '''
        cell = args[0][0]
        cell.get_Type().config(bg = "green")
    
    def InitializeTable(self,Type,color,player,frame = None,StartPosition = None):
        '''
        
        :param Type: UI or GUI because they are different types of entities
        :param color: the color of the table (it s different for the player and the AI)
        :param player: AI or NAI meaning that it is AI or not
        :param frame: if the type of the table is GUI then it needs a frame on what tkinter it's going to place all the buttons
        :param StartPosition: if the type of the table is GUI then the position of the Buttons will differ based on what table they belong
        
        :return ---
            the tables will be initialized with entities that represent that every cell is not a plane
        '''
        for i in range(8):
            for j in range(8):
                if Type == "ui":
                    cell = ButtonForRepo("0",i,j,color,player)
                else:
                    button = Button(frame,bg = color,text = "",fg = color)
                    button.grid(row = i, column = j+StartPosition)
                    button.config(height = 3, width = 6)
                    cell = ButtonForRepo(button,i,j,color,player)
                    
                    if player == "NAI":
                        event = partial(self.GuiAddPlayerPlane,[i,j,"gui",color,player,frame])
                        button.bind("<Button-1>",event)
                        
                        event = partial(self.NotPlane,[cell,frame])
                        button.bind("<Button-2>",event)
                    else:
                        event = partial(self.HitNotPlane,[cell,frame])
                        button.bind("<Button-1>",event)
                    
                if player == "NAI":
                    self.__player_table.Initialize(cell)
                else:
                    self.__ai_table.Initialize(cell)

    def AddAiPlane(self, row, column,Type,frame = None):
        '''        
        :param row: 
        :param column:
                    these 2 represent the random position where the AI plane will have it's cockpit  
        :param Type: UI or GUI because they are different types of entities
        :param frame: if the type of the table is GUI then it needs a frame on what tkinter it's going to place all the buttons
        
        :return ----
                it will add on the corresponding positions of cells that will be part of the plane that has the cockpit 
                on the position given entities that will say that the positions are part of a plane 
        '''
        row_neighbours = [0,-2,-1,0,1,2,0,-1,0,1]
        column_neighbours = [0, 1, 1,1,1,1,2, 3,3,3]
        
        to_remove = []
        
        number_of_choises = len(self.__choice)
        index1 = 0 
        while index1 < number_of_choises:
            index2 = 0
            ok = False
            while index2 < 10 and ok != True: 
                index3 = 0 
                while index3 < 10 and ok != True:
                    if (self.__choice[index1][0] + row_neighbours[index2]) == (row + row_neighbours[index3]):
                        if (self.__choice[index1][1] + column_neighbours[index2]) == (column + column_neighbours[index3]):
                            to_remove.append(self.__choice[index1])
                            ok = True
                    index3 += 1
                index2 += 1
            index1 += 1

        for i in to_remove:
            self.__choice.remove(i)
        row_copy = copy.deepcopy(row)
        column_copy = copy.deepcopy(column)
        
        if Type == "ui":
            for i in range(len(row_neighbours)):
                if i != 0:
                    cell = ButtonForRepo("0", row + row_neighbours[i] , column + column_neighbours[i], "blue", "AI")
                else:
                    cell = ButtonForRepo("0", row + row_neighbours[i] , column + column_neighbours[i], "pink", "AI")
                
                self.__ai_table.AddSingleEntity(cell)
        else:
            for i in range(len(row_neighbours)):
                button = Button(frame,bg = "white" ,text = "-",fg = "white")
                button.grid(row = row_copy + row_neighbours[i] , column = column_copy + column_neighbours[i] + 30)
                button.config(height = 3, width = 6)
                
                cell = ButtonForRepo(button,row_copy+ row_neighbours[i],column_copy+ column_neighbours[i],"blue","AI")
                #cell.hit_plane()
                if i != 0:
                    event = partial(self.HitPlane,[cell,frame])
                else:
                    event = partial(self.HitCockpit,[cell,frame])
                #button.unbind("<Button-1>")
                button.bind("<Button-1>",event)
    
    def HitPlayer(self,interface):
        '''        
        :param interface: UI or GUI because they are different types of entities
        
        :return ----
                the AI will attack a random position from the ones that it know that are valid for placing a cockpit
                if the interface it s not GUI then i need to explain for every kind of entity (cockpit , plane , notPlane)
                    what it should be doing
        '''
        row_neighbours = [0,-2,-1,0,1,2,0,-1,0,1]
        column_neighbours = [0, 1, 1,1,1,1,2, 3,3,3]
        if len(self.__thinking_choice) == 0:
            position = random.choice(self.__choice)
        else:
            position = self.__thinking_choice[0]
            
        if interface == "ui":
            row = position[0]
            column = position[1]
            table = self.__player_table.get_all()
            if table[row][column].get_color() == "blue":
                table[row][column].set_Type("X")
            elif table[row][column].get_color() == "pink":
                self.__player_planes_down += 1
                for i in range(len(row_neighbours)):
                    table[row + row_neighbours[i]][column + column_neighbours[i]].set_Type("X")
                if self.__player_planes_down == 2:
                    return -1
                    #print("You lost")
            else:
                table[row][column].set_Type("-")
        else:
            row = position[0]
            column = position[1]
            table = self.__player_table.get_all()
            table[row][column].get_Type().event_generate("<Button-2>")
            if table[row][column].get_Type()["bg"] == "red":
                if [row,column-3] in self.__choice and [row,column-3] not in self.__thinking_choice:
                    self.__thinking_choice.append([row,column-3])
                if [row-1,column-3] in self.__choice and [row-1,column-3] not in self.__thinking_choice:
                    self.__thinking_choice.append([row-1,column-3])
                if [row+1,column-3] in self.__choice and [row+1,column-3] not in self.__thinking_choice:
                    self.__thinking_choice.append([row+1,column-3])
                if [row,column-2] in self.__choice and [row,column-2] not in self.__thinking_choice:
                    self.__thinking_choice.append([row,column-2])
                if [row,column-1] in self.__choice and [row,column-1] not in self.__thinking_choice:
                    self.__thinking_choice.append([row,column-1])
                if [row-1,column-1] in self.__choice and [row-1,column-1] not in self.__thinking_choice:
                    self.__thinking_choice.append([row-1,column-1])
                if [row-2,column-1] in self.__choice and [row-2,column-1] not in self.__thinking_choice:
                    self.__thinking_choice.append([row-2,column-1])
                if [row+1,column-1] in self.__choice and [row+1,column-1] not in self.__thinking_choice:
                    self.__thinking_choice.append([row+1,column-1])
                if [row+2,column-1] in self.__choice and [row+2,column-1] not in self.__thinking_choice:
                    self.__thinking_choice.append([row+2,column-1])
        #print(self.__thinking_choice)
        #print(position)
        self.__choice.remove(position)
        if len(self.__thinking_choice) != 0:
            del self.__thinking_choice[0]
    
    def close(self,*args):
        '''
        args = the frame we need to close (GUI)
        '''
        args[0].quit()
    
    def HitCockpit(self,*args):            
        '''
        :args the position of the cell
            this is for the AI table and just for GUI 
            it's the event that occurs when a button that is a cockpit of a plane is clicked
        '''
        row = args[0][0].get_row()
        column = args[0][0].get_column()
        self.__thinking_choice = []
        self.__ai_planes_down += 1
        
        row_neighbours = [0,-2,-1,0,1,2,0,-1,0,1]
        column_neighbours = [0, 1, 1,1,1,1,2, 3,3,3]
        
        for i in range(len(row_neighbours)):
            button = Button(args[0][1],bg = "red",text = "-", fg = "white")
            button.grid(row = row + row_neighbours[i], column = column + column_neighbours[i] + 30)
            button.config(height = 3 , width = 6)
            cell = ButtonForRepo(button , row + row_neighbours[i], column + column_neighbours[i], "red","AI")
        
        self.__ai_table.AddSingleEntity(cell,args[0][1],30)
        
        if self.__ai_planes_down == 2:
            button = Button(args[0][1],bg = "yellow",text = "You won!", fg = "black")
            button.grid(row = 3 , column = 7)
            button.config(height = 3, width = 6)

            args[0][1].after(1000,self.close,args[0][1])
            #print("You won")
            #return
        
        self.HitPlayer("gui")
        
    def HitPlane(self,*args):
        '''
        :args the position of the cell
            this is for the AI table and just for GUI 
            it's the event that occurs when a button that is part of a plane is clicked
        '''
        row = args[0][0].get_row()
        column = args[0][0].get_column()
        
        button = Button(args[0][1],bg = "red",text = "-", fg = "white")
        button.grid(row = row , column = column + 30)
        button.config(height = 3 , width = 6)
        cell = ButtonForRepo(button , row, column, "red","AI")
        
        self.__ai_table.AddSingleEntity(cell,args[0][1],30)
        self.HitPlayer("gui")
    
    def HitNotPlane(self,*args):
        '''
        :args the position of the cell
            this is for the AI table and just for GUI 
            it's the event that occurs when a button that is not part from a plane is clicked
        '''
        row = args[0][0].get_row()
        column = args[0][0].get_column()
        
        button = Button(args[0][1],bg = "green",text = "", fg = "white")
        button.grid(row = row , column = column + 30)
        button.config(height = 3 , width = 6)
        cell = ButtonForRepo(button , row, column, "green","AI")
        
        self.__ai_table.AddSingleEntity(cell,args[0][1],30)
        self.HitPlayer("gui")
        
        
    def Reset(self,Type,frame = None):
        '''
        
        :param Type: UI or GUI because they are different types of entities
        :param frame: if the type of the table is GUI then it needs a frame on what tkinter it's going to place all the buttons
            when this method is called all the tables are reseted from the begging
        '''
        self.__choice = [[2,0],[2,1],[2,2],[2,3],[2,4],
                         [3,0],[3,1],      [3,3],[3,4],
                         [4,0],[4,1],      [4,3],[4,4],
                         [5,0],[5,1],[5,2],[5,3],[5,4]]
        self.__ai_planes_down = 0
        self.__player_planes_down = 0
        if Type == "ui":
            self.InitializeTable("ui","grey","NAI")
            self.InitializeTable("ui","white","AI")
            self.RandomizeAiPlanes("ui")
        else :
            self.InitializeTable("gui","grey","NAI",frame,0)
            self.InitializeTable("gui","white","AI",frame,30)
            self.RandomizeAiPlanes("gui",frame)
            
    def RandomizeAiPlanes(self,Type,frame = None):
        '''
        
        :param Type: UI or GUI because they are different types of entities
        :param frame: if the type of the table is GUI then it needs a frame on what tkinter it's going to place all the buttons
                this method make randomly a choice from the only possibles positions of a cockpit so it will set there a plane for the AI
                and based on that first choice it removed invalid positions
        '''
        try :
            position = random.choice(self.__choice)
            row = position[0] 
            column = position[1]
        except IndexError:
            self.Reset(Type, frame)
        
        self.AddAiPlane(row,column,Type,frame)
        #print(self.__choice)
        try:
            position = random.choice(self.__choice)
            row = position[0] 
            column = position[1]
        except IndexError:
            self.Reset(Type, frame)

        self.AddAiPlane(row,column,Type,frame)
            
        self.__choice = [[2,0],[2,1],[2,2],[2,3],[2,4],
                         [3,0],[3,1],      [3,3],[3,4],
                         [4,0],[4,1],      [4,3],[4,4],
                         [5,0],[5,1],[5,2],[5,3],[5,4]]
    
    def GuiAddPlayerPlane(self,*args):
        '''
        :row = args[0][0]
        :column = args[0][1]
        :Type = args[0][2]
        :color = args[0][3]
        :player = args[0][4]
        :frame = args[0][5]
            it's the event triggered when you click on a Player cell
        '''
        
        row = args[0][0]
        column = args[0][1]
        Type = args[0][2]
        color = args[0][3]
        player = args[0][4]
        frame = args[0][5]
        
        try:
            self.AddPlayerPlane(row, column, Type, color, player, frame)
        except RepoError:
            pass

    def PlayerPlaneHited(self,*args):
        '''
        :cell = args[0][0] the cell is an entity 
            it's the event that triggers when the AI choses a cell in which is a plane part
        '''
        cell = args[0][0]   
        cell.get_Type().config(bg = "red")
    
    
    def PlayerPlaneDown(self,*args):
        '''
        :cell = args[0][0] the cell is an entity 
            it's the event that triggers when the AI choses a cell which is the plane cockpit
        '''
        cell = args[0][0]
        row = cell.get_row()
        column = cell.get_column()  
        row_neighbours = [0,-2,-1,0,1,2,0,-1,0,1]
        column_neighbours = [0, 1, 1,1,1,1,2, 3,3,3]
        
        for i in range(len(row_neighbours)):
            entity = self.__player_table.get_entity(row + row_neighbours[i] , column + column_neighbours[i])
            entity.get_Type().config(bg = "red")
        
        self.__player_planes_down += 1
        
        if self.__player_planes_down == 2:
            button = Button(args[0][1],bg = "yellow",text = "You lost!", fg = "black")
            button.grid(row = 3 , column = 7)
            button.config(height = 3, width = 6)

            args[0][1].after(1000,self.close,args[0][1])

    
    
    def AddPlayerPlane(self,row,column,Type,color,player,frame = None):
        '''
        
        :param row:
        :param column:
                these 2 make the position that the player choses for the cockpit of one of it's 2 planes 
        :param Type: UI or GUI because they are different types of entities
        :param color: the color of the table (it s different for the player and the AI)
        :param player: AI or NAI meaning that it is AI or not
        :param frame: if the type of the table is GUI then it needs a frame on what tkinter it's going to place all the buttons
            
            the method will make the positions corresponding to the plane based on the position of the cockpit to be part of the plane
        '''
        row_neighbours = [0,-2,-1,0,1,2,0,-1,0,1]
        column_neighbours = [0, 1, 1,1,1,1,2, 3,3,3]
        
        position = [row,column]
        if position not in self.__choice:
            return
        
        if Type == "ui":
            for i in range(len(row_neighbours)):
                if self.__player_table.get_entity(row+row_neighbours[i],column+column_neighbours[i]).get_Type() != "0":
                    return
            for i in range(len(row_neighbours)):
                if i == 0:
                    cell = ButtonForRepo("1",row+row_neighbours[i],column+column_neighbours[i],"pink",player)
                else:
                    cell = ButtonForRepo("1",row+row_neighbours[i],column+column_neighbours[i],"blue",player)
                self.__player_table.AddSingleEntity(cell)
        else:
            for i in range(len(row_neighbours)):
                if self.__player_table.get_entity(row+row_neighbours[i],column+column_neighbours[i]).get_Type()["bg"] == "blue":
                    return
            for i in range(len(row_neighbours)):
                button = Button(frame,bg = "blue",text = "",fg = "blue")
                cell = ButtonForRepo(button,row+row_neighbours[i],column+column_neighbours[i],"blue",player)
                if i != 0 :
                    event = partial(self.PlayerPlaneHited,[cell,frame])
                else:
                    event = partial(self.PlayerPlaneDown,[cell,frame])
                button.bind("<Button-2>",event)
                self.__player_table.AddSingleEntity(cell,frame)

    
    def HitAi(self,row,column):
        '''
        :param row:
        :param column:
            these 2 make the position in which the player will attack (just for UI)
            and based on the "color" of the cell it's know that it a plane, a cockpit or a free position
        '''
        if self.__ai_table.get_entity(row,column).get_color() == "blue":
            self.__ai_table.get_entity(row,column).set_Type("X")
            self.__ai_table.get_entity(row,column).set_color("X")
        elif self.__ai_table.get_entity(row,column).get_color() == "pink":
            row_neighbours = [0,-2,-1,0,1,2,0,-1,0,1]
            column_neighbours = [0, 1, 1,1,1,1,2, 3,3,3]
            self.__ai_planes_down += 1
            for i in range(len(row_neighbours)):
                self.__ai_table.get_entity(row + row_neighbours[i], column + column_neighbours[i]).set_color("X")
                self.__ai_table.get_entity(row + row_neighbours[i], column + column_neighbours[i]).set_Type("X")
            if self.__ai_planes_down == 2:
                return 1
                #print("You won!")
        elif self.__ai_table.get_entity(row,column).get_color() != "X":
            self.__ai_table.get_entity(row,column).set_color("X")
            self.__ai_table.get_entity(row,column).set_Type("-")
        self.HitPlayer("ui")
        