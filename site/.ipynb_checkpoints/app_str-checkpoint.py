import streamlit as st
import pandas as pd
import sqlite3
from EAC import site
conn = sqlite3.connect('training.db')
st.write("Test for the app!")
st.write("Day:")
st.selectbox('Choose Day:',)
st.subheader("Primary Work:")
train = pd.read_sql('''select * from
upcommingTraining
where ''',conn)
st.subheader("Secondary Work:")

st.dataframe(train)