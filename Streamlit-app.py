from vanna.openai import OpenAI_Chat
from vanna.vannadb import VannaDB_VectorStore
import streamlit as st

class MyVanna(VannaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        # Fetch secrets from st.secrets
        MY_VANNA_MODEL = st.secrets.vanna.vanna_model_name
        MY_VANNA_API_KEY = st.secrets.vanna.vanna_api_key
        MY_OPENAI_API_KEY = st.secrets.openai.openai_api_key

        # Initialize VannaDB_VectorStore and OpenAI_Chat with secrets
        VannaDB_VectorStore.__init__(self, vanna_model=MY_VANNA_MODEL, vanna_api_key=MY_VANNA_API_KEY, config=config)
        OpenAI_Chat.__init__(self, config={'api_key': MY_OPENAI_API_KEY, 'model': config.get('model', 'gpt-4')})

# Use the MyVanna class with secrets
vn = MyVanna(config={'model': 'gpt-4'})


vn.connect_to_postgres(host='localhost', dbname='Employees', user='postgres', password='sys@123', port='5432')


my_question = st.session_state.get("my_question", default=None)
if my_question == None:
    my_question = st.text_input(
        "Ask me a question about your data",
        key="my_question",
    )
else:
    st.text(my_question)
    
    sql = vn.generate_sql(my_question)

    st.text(sql)

    df = vn.run_sql(sql)    
        
    st.dataframe(df, use_container_width=True)

    code = vn.generate_plotly_code(question=my_question, sql=sql, df=df)

    fig = vn.get_plotly_figure(plotly_code=code, df=df)

    st.plotly_chart(fig, use_container_width=True)

