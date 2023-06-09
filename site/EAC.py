import pandas as pd
import os

class training():
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

class cardio ():
    '''
    This will track active steps and bike riding that is done.
    '''

class database():
    def __init__(self):
        conn = sqlite3.connect('training.db')
    
    def meso_load(self):    
        files = [f for f in os.listdir('../data/uploads')]
        