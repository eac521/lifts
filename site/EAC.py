import pandas as pd
import os
import sqlite3

class training:
    '''
    This will be the class that houses the lifting data. So velocity history/show, Meso training log, meso creation, warm-up calc,
    '''         
            
    #def split(self) add in later when we will want this with more flexibility on different types of splits
    def show_today(self):
        '''
        this will be the primary output for what is shown on the page
        '''
    def plot_velo(self):
        '''
        Show prior velocity training ressults
        '''
    def warmup(self):
        '''
        get warmup calculator to setup our warmup sets for the initial lift
        '''

class cardio:
    '''
    This will track active steps and bike riding that is done.
    '''

class database:
    '''
    To be used to updated database information, will auto connect when instantiated

    '''
    def __init__(self):
        conn = sqlite3.connect('training.db')

    def update_program(self,rowData,connection):
        for ct,row in enumerate(rowData):
            str(ct)+row[0]

