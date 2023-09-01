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
        self.conn = sqlite3.connect('training.db')
        
    def add_data(self,data,table):
        with open(data,'r') as d:
            for i,row in enumerate(d):
                if i==0:
                    continue
                else:
                    print(row)
                    row = row.replace('\n','')
                    qs = (len(row.split(','))-1)*'?,'+'?'
                    self.conn.execute('''INSERT into {t} values ({row})'''.format(t=table,row=qs),row.split(','))
            self.conn.commit()
        return '{} has been updated with {} rows of data'.format(table,i)
    
    def create_meso_cycle(self,file):
        df = pd.DataFrame(columns = ['movement','method','week','sets','reps','weight','notes','targetReps'])
        prgbld = pd.read_sql('''
        select * 
        from programBuilder
        ''',conn)
        mesoDF = pd.read_csv(file).fillna(0)
        v = df.columns[-5:].values
        r=0
        for sesh in mesoDF.session.unique():
            d = mesoDF[mesoDF.session == sesh]
            for movement in d.exercise.unique():
                endweek = d[d.exercise==movement].endWeek.values[0]
                mod = d[d.exercise==movement].modality.values[0]
                cyclelength = prgbld[prgbld.method==mod].week.max()
                setAdjust = d[d.exercise==movement].SetAdjust.values[0]
                print(movement,mod,setAdjust)
                for i in range(endweek):
                    lkup = i+1 if cyclelength==endweek else (i+1) % cyclelength
                    lkup = cyclelength if lkup == 0 else lkup
                    l = [movement,mod,i+1]+prgbld[(prgbld.method==mod) & (prgbld.week==lkup)].filter(v).values.tolist()[0]
                    df.loc[len(df)] = l
                    df.at[r,'sets'] = df.at[r,'sets'] + setAdjust
                    r+=1
        with self.conn as connection:
            add_data(df.values,'upcomingTraining')

            
            
            
            
            
            
            
            
            
            

