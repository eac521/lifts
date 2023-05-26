from shiny import App, render, ui,reactive
import pandas as pd
import string
import numpy as np

app_ui = ui.page_fluid(
    ui.input_numeric("yr","Year",value=2022),
    ui.row(
    ui.column(2,ui.output_table("standings")),
    ui.column(3,ui.output_table("breakout"))


)
)

def server(input, output, session):

    @reactive.Calc
    def getBase():
        yr = str(input.yr())
        sheet_id = '1YaNuDloijTRKkys9TZsfGaH7N3eCie3zTCmw1t-8SAA'
        sheet_name = yr
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        draft = pd.read_csv(url).iloc[:, :2]
        team, info = pd.read_html('https://www.espn.com/nfl/standings/_/season/' + yr + '/group/league')

        f = team.columns.to_frame(index=0, name='team')
        team.columns = ['team']
        df = pd.concat([f, team]).reset_index(drop=True)
        df = df.merge(info, left_index=True, right_index=True)
        if df.filter(['W', 'L', 'T']).sum(axis=1).max() > 10 and df.filter(['W', 'L', 'T']).sum(axis=1).nunique() == 1:
            week = df.filter(['W', 'L', 'T']).sum(axis=1).max() + 1
        else:
            week = df.filter(['W', 'L', 'T']).sum(axis=1).max()

        df['week'] = week
        df['team'] = [team if team.find('--') == -1 else team[team.find('--') + 2:] for team in df.team]
        abbrev = [''.join([cap for cap in team.split()[0] if cap in string.ascii_uppercase][:-1]) for team in df.team]
        df['abbrev'] = abbrev
        df['team'] = [df.team[i].replace(df.abbrev[i], '') for i in range(len(df))]
        draft = draft.rename(columns={'Picked': 'abbrev'})
        df = df.merge(draft)
        return df
    @output
    @render.table()
    def breakout():
        df= getBase()
        piv = pd.pivot_table(df, index=['Teams', 'team'], values=['DIFF', 'W'], aggfunc='sum').reindex(['W', 'DIFF'],axis=1)
        grp = piv.groupby('Teams').sum()
        piv['order'] = 1
        grp['team'] = 'Total'
        grp['order'] = 4
        grp = grp.reset_index().set_index(['Teams', 'team'])
        piv = piv.append(grp).sort_values(by=['Teams', 'order', 'W', 'DIFF'], ascending=[True, True, False, False])
        piv.drop(columns=['order'], inplace=True)
        piv.reset_index(inplace=True)
        piv['Teams'] = np.where(piv.groupby('Teams').cumcount() == 0, piv.Teams, '')
        return piv
    @output
    @render.table()
    def standings():

        base = getBase()
        total  = base.filter(['W','PF','PA','DIFF','Teams']).groupby('Teams').sum().reset_index()
        return total.sort_values(by=['W','DIFF'],ascending=[False,False])
app = App(app_ui, server)
