import os 
import pandas as pd
import numpy as np
import re
import sqlite3

conn = sqlite3.connect('./site/training.db')
def create_meso_cycle(path,connection):
    df = pd.DataFrame(columns = ['movement','method','week','sets','reps','weight','notes','targetReps'])
    prgbld = pd.read_sql('''
    select methodID, lower(method) as method, week, sets,reps,weight,notes,targetReps
    from programBuilder
    ''',conn)
    mesoDF = pd.read_csv(dataPath+trainingFile).fillna(0)
    maxes = pd.read_sql('''
    select movement,actualMax
    from movements
    ''',conn)
    v = df.columns[-5:].values
    r=0
    for sesh in mesoDF.session.unique():
        d = mesoDF[mesoDF.session == sesh]
        for movement in d.exercise.unique():
            endweek = d[d.exercise==movement].endWeek.values[0]
            mod = d[d.exercise==movement].modality.values[0]
            cyclelength = prgbld[prgbld.method==mod].week.max()
            setAdjust = d[d.exercise==movement].SetAdjust.values[0]
            for i in range(endweek):
                lkup = i+1 if cyclelength==endweek else (i+1) % cyclelength
                lkup = cyclelength if lkup == 0 else lkup
                l = [movement,mod,i+1]+prgbld[(prgbld.method==mod) & (prgbld.week==lkup)].filter(v).values.tolist()[0]
                df.loc[len(df)] = l
                df.at[r,'sets'] = df.at[r,'sets'] + setAdjust
                r+=1
    final = df[['movement','method']].drop_duplicates().reset_index(drop=True)
    final.movement = final.movement.str.lower()
    final = final.merge(maxes,how='left',on='movement')
    for wk in df.week.unique():
        final['sets{}'.format(wk)] = df[df.week==wk].sets.values
        final['reps{}'.format(wk)] = df[df.week==wk].reps.values
        final['weight{}'.format(wk)] = df[df.week==wk].weight.values
        final['targetReps{}'.format(wk)] = df[df.week==wk].targetReps.values
    
    path = './site/initialData/meso_file.csv'
    final.to_csv(path)
    return final,path
def add_data(path,table,connection,insert=False):
    if insert:
        cols = pd.read_sql('select * from {} limit 1'.format(table),conn).columns
        qs = (len(cols)-1)*'?,'+'?'
        connection.execute('''INSERT into {t} values ({row})'''.format(t=table,row=qs),path)
        i = 1
    else:
        with open(path,'r') as d:
            for i,row in enumerate(d):
                if i==0:
                    continue
                else:
                    row = row.replace('\n','')
                    qs = (len(row.split(','))-1)*'?,'+'?'
                    connection.execute('''INSERT into {t} values ({row})'''.format(t=table,row=qs),row.split(','))
    
    connection.commit()
    print('{} has been updated with {} rows of data'.format(table,i))
    

def update_movements_table(training_path,conn):
    '''
    Will take a csv of the training file, will find differences and update the database
    '''
    training = pd.read_csv('./InitialData/training - TrainingCopy.csv',skiprows=1)
    training.movement = training.movement.str.lower()
    df = training.filter(['movement']+[col for col in training.columns if col.find('wrk')>-1])
    df = df.dropna().set_index('movement')
    mvmts = '","'.join(df.index.str.lower().values)
    mvmt = pd.read_sql('''select * from movements where movement in ("{}")'''.format(mvmts),conn)
    ct=0
    for lft in df.index.values:
    
        lft = lft.lower()
        print(lft)
        try:
            if lft not in mvmt.movement.str.lower().values:
                print('\tAdding into movements table'.format(lft))
                d = [lft,None,df.loc[lft]['wrk_10']] + [np.nan] * (len(mvmt.columns) - 3)
                add_data(d,'movements',conn,True)
                ct+=1
            else:
                print('\tHave {} in database table'.format(lft))
        except:
            print('\t{} NOT ADDED'.format(lft.upper()))
        try:
            if df.loc[lft]['wrk_10'] != mvmt[mvmt.movement==lft]['actualMax'].values[0]:
                print('\tNew working max')
                conn.execute('''UPDATE movements
                        SET actualMax = {0} where movement = "{1}" '''.format(df.loc[lft]['wrk_10'],lft))
            ct+=1
        except:
            print('\tMax same as prior meso') 
        conn.commit()
    print('updated movements table with {} edits'.format(ct))

_,path,prgname = max([(os.stat(f)[-1],f.path,f.name) for f in os.scandir('./site/InitialData/') if re.search('PPL.csv$',f.name)!=None])
_,history,histname = max([(os.stat(f)[-1],f.path,f.name) for f in os.scandir('./site/InitialData/') if re.search('TrainingCopy.csv$',f.name)!=None])
print('Have {} found for upcoming training and {} loading history'.format(prgname,histname))
update_movements_table(history,conn)
create_meso_cycle(path,conn)
print('All updates are complete get new file')