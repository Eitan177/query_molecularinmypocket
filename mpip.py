import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import pickle
import numpy as np
import streamlit as st
from streamlit_pdf_reader import pdf_reader
from lucknowllm import GeminiModel
import random


st.set_page_config(layout="wide")

gem_key1 = st.secrets["api_keys"]["gemini1"]
gem_key2 = st.secrets["api_keys"]["gemini2"]
gem_key3 = st.secrets["api_keys"]["gemini3"]
gem_key4 = st.secrets["api_keys"]["gemini4"]
gem_key5 = st.secrets["api_keys"]["gemini5"]
gem_key6 = st.secrets["api_keys"]["gemini6"]

with open('mpip.pkl', 'rb') as f:
    keys_for_tables,tables = pickle.load(f)
    keys_for_tables_uniques = np.unique(keys_for_tables)
st.title('Molecular in My Pocket Query App')    

def displaydata(dfshow,tablename):

    maketab=np.arange(0,len(dfshow)).astype(str).tolist()
    maketab=['Table '+str(i[0])+' '+str(i[1]) for i in zip(maketab,tablename) ]
    tabs = st.tabs(maketab)
    for indexshow,(i,n,table_n) in enumerate(zip(tabs,maketab,tablename)):
        with i:
            df = dfshow[indexshow]
            st.write(df)
            #st.write(table_n)
            questionfortable=st.text_input('Question about the table? see if gemini can answer-','',key='llm'+n)
            alltableq = st.radio('aski gemini this question for every table from the current query result ('+str(len(dfshow))+' tables)',[False,True])
            showchecked=st.checkbox('show pdf?',key='checked'+n)
            if questionfortable != '' and alltableq:
                gem_key=[gem_key1, gem_key2, gem_key3, gem_key4,gem_key5,gem_key6][random.randint(0, 5)] 
                Gemini=GeminiModel(api_key = gem_key, model_name = "gemini-1.0-pro")
                for j,current_df in enumerate(dfshow):
                    argumented_prompt = f"You are an expert question answering system, I'll give you question and context and you'll return the answer. Query : {questionfortable} Contexts : { current_df.to_string(index=False)}"
                    model_output = Gemini.generate_content(argumented_prompt)
                    st.write('Answer using table '+str(j))
                    st.write(model_output)
            elif questionfortable !='':
                gem_key=[gem_key1, gem_key2, gem_key3, gem_key4,gem_key5,gem_key6][random.randint(0, 5)] 
                Gemini=GeminiModel(api_key = gem_key, model_name = "gemini-1.0-pro")
                argumented_prompt = f"You are an expert question answering system, I'll give you question and context and you'll return the answer. Query : {questionfortable} Contexts : { df.to_string(index=False)}"
                model_output = Gemini.generate_content(argumented_prompt)
                st.write(model_output)                
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

if len(tablename) > 0:
  displaydata(dfshow,tablename)   
else:
  st.write('nothing found') 
      


