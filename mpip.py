import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import pickle
import numpy as np
import streamlit as st
from streamlit_pdf_reader import pdf_reader
st.set_page_config(layout="wide")



with open('mpip.pkl', 'rb') as f:
    keys_for_tables,tables = pickle.load(f)
    keys_for_tables_uniques = np.unique(keys_for_tables)
st.title('Molecular in My Pocket Query App')    

def displaydata(dfshow,tablename):

    maketab=np.arange(0,len(dfshow)).astype(str).tolist()
    maketab=['Table '+str(i[0])+' '+str(i[1]) for i in zip(maketab,tablename) ]
    tabs = st.tabs(maketab)
    for i,n,table_n in zip(tabs,maketab,tablename):
        with i:
            df = dfshow.pop(0)
            st.write(df)
            #st.write(table_n)
            showchecked=st.checkbox('show pdf?',key='checked'+n)
            if showchecked:
              st.write(n)
              pdf_reader('https://www.amp.org/AMP/assets/File/education/MIMP/'+str(table_n)+'.pdf',key=n)



table_to_view=st.selectbox('Select a table', keys_for_tables_uniques)
st.write('or')
searchtext=st.text_input('Search', '')
st.write('tables may be searched by text in any column. All tables containing the input text will be displayed. Alternatively, tables may searched using the dropdown and selecting an entity')
dfshow=[]
dfshowtextsearch=[]
tablename=[]
if searchtext != '':
    for table,key in zip(tables,keys_for_tables):
        tablefindtext=table[table.apply(lambda row: searchtext.lower() in row.astype(str).str.lower().str.cat(sep=' '), axis=1)]
        if tablefindtext.shape[0]>0:
            dfshow.append(tablefindtext)
            tablename.append(key)


else:
    for table,key in zip(tables,keys_for_tables):
        if key==table_to_view:
            dfshow.append(table)
            tablename.append(key)
displaydata(dfshow,tablename)        


