from Entities import ButtonForRepo
from Erros import RepoError
from tkinter import *
import copy
from _functools import partial

class PlayTable(object):
    def __init__(self):
        self.__buttons = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    
    def Initialize(self,entity):
        '''
        
        :param entity:
        
            it add no matter what the entity on it's position
        '''
        self.__buttons[entity.get_row()][entity.get_column()] = entity
    
    def AddSingleEntity(self,entity,frame = None,startpos = 0 ):
        '''
        
        :param entity:
        :param frame: if we have GUI
        :param startpos: if we have GUI
        
            it adds the entity and if we have a GUI the entity , using grid , is made visible to the user
        '''
        self.__buttons[entity.get_row()][entity.get_column()] = entity
        if frame != None:
            self.__buttons[entity.get_row()][entity.get_column()].get_Type().grid(row = entity.get_row(),column = entity.get_column() + startpos)
            self.__buttons[entity.get_row()][entity.get_column()].get_Type().config(height = 3, width = 6)
    
    def get_entity(self,row,column):
        '''
        :param row:
        :param column:
            :return the entity that has the specified position
        '''
        return self.__buttons[row][column]
    
    def get_all(self):
        '''
        :return all the entities existent in our repository
        '''
        return self.__buttons