class ButtonForRepo(object):
    def __init__(self,Type,row,column,color,player):
        self.__Type = Type
        self.__row = row
        self.__column = column
        self.__color = color
        self.__player = player
    
    def get_color(self):
        '''
        
        '''
        return self.__color
    
    def set_color(self,new_color):
        '''
        
        :param new_color:
        '''
        self.__color = new_color
    
    def get_Type(self):
        '''
        
        '''
        return self.__Type
    
    def set_Type(self,new_type = None):
        '''
        
        :param new_type:
        '''
        if new_type == None:
            self.__Type.config(bg = "blue")
        else:
            self.__Type = new_type
        #self.__color = "blue"
    
    def get_row(self):
        '''
        
        '''
        return self.__row
    
    def set_row(self,new_row):
        '''
        
        :param new_row:
        '''
        self.__row = new_row
    
    def get_column(self):
        '''
        
        '''
        return self.__column
    
    def set_column(self,new_column):
        '''
        
        :param new_column:
        '''
        self.__column = new_column
    
    def hit_plane(self):
        '''
        
        '''
        #print("I m here but i m retarded")
        self.__Type.config(bg = "red",fg = "red")
        self.__color = "red"
    
    def hit_not_plane(self):
        '''
        
        '''
        self.__Type.config(bg = "green")
    
    def __eq__(self,entity):
        row_nieghbours =    [0,-2,-1,0,1,2,0,-1,0,1]
        column_neighbours = [0, 1, 1,1,1,1,2, 3,3,3]
        
        for i in range(len(row_nieghbours)):
            if (entity.__row + row_nieghbours[i]) == self.__row :
                if (entity.__column + column_neighbours[i]) == self.__column:                   
                    if self.__color == entity.__color:
                        return True
                    else:
                        if type(self.__Type) != str:
                            if self.__Type["bg"] == entity.__Type["bg"]:
                                return  True
        return False
    def __str__(self):
        return self.__Type + " "