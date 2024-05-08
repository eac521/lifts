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
    mesoDF = pd.read_csv(path).fillna(0)
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
    path = './site/initialData/meso_file.csv'
    df.to_csv(path)
    return df,path
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
    training = pd.read_csv(training_path,skiprows=1)
    training.movement = training.movement.str.lower()
    df = training.filter(['movement']+[col for col in training.columns if col.find('wrk')>-1])
    df = df.dropna().set_index('movement')
    mvmts = '","'.join(df.index.values)
    mvmt = pd.read_sql('''select * from movements where movement in ("{}")'''.format('","'.join(mvmts)),conn)
    ct=0
    for lft in df.index.values:
        try:
            if lft not in mvmt.movement.values:
                print('Adding in {} into movements table'.format(lft))
                d = [lft] + [np.nan] * (len(mvmt.columns) - 1)
                add_data(d,'movements',conn,True)
                ct+=1
            elif df.loc[lft]['wrk_10'] != int(mvmt[mvmt.movement=='convo']['actualMax'].values[0]):
                conn.execute('''UPDATE movements
                                    SET actualMax = {0} where movement = {1}'''.format(df.loc[lft]['wrk_10'],lft))
                ct+=1
            conn.commit()
        except:
            print('error')
    print('updated movements table with {} edits'.format(ct))

_,path,prgname = max([(os.stat(f)[-1],f.path,f.name) for f in os.scandir('./site/InitialData/') if re.search('PPL.csv$',f.name)!=None])
_,history,histname = max([(os.stat(f)[-1],f.path,f.name) for f in os.scandir('./site/InitialData/') if re.search('TrainingCopy.csv$',f.name)!=None])
print('Have {} found for upcoming training and {} loading history'.format(prgname,histname))
update_movements_table(history,conn)
create_meso_cycle(path,conn)
print('All updates are complete get new file')