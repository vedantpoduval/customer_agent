import streamlit as st
from vector_store import FlowerShopVector
from langchain_core.messages import AIMessage,HumanMessage
from chatbot import app

# vector_store = FlowerShopVector()

st.set_page_config(page_title="flower shop chatbot",page_icon="🌻",layout="wide")

if 'message_history' not in st.session_state:
    st.session_state.message_history = [AIMessage(content = "Hey , I am the flower shop chatbot how can I help")]


left_column,main_column,right_column = st.columns([1,2,1])

# 1.Buttons for chat - Clear button(first column)
with left_column:
    if st.button('Clear Chat'):
        st.session_state.message_history = []
    # collection_choice = st.radio("Which Collection?",['FAQs','Inventories'])
 
# 2.Chat history and input        
with main_column:
    user_input = st.chat_input('Enter your chat')
    if user_input:
        # # st.text(user_input)
        # if collection_choice == "FAQs":
        #     related_questions = vector_store.query_faqs(query=user_input)
        # else:
        #     related_questions = vector_store.query_inventories(query=user_input)
        
        st.session_state.message_history.append(HumanMessage(content=user_input))
        response = app.invoke({
              'messages': st.session_state.message_history
                }
                )
        # print(response)
        st.session_state.message_history = response['messages']
        # st.session_state.message_history.append({'content': related_questions,'type':'assistant'})
            

    for message in reversed(st.session_state.message_history):
        if isinstance(message,AIMessage):
            message_box = st.chat_message('assistant')
        else:
            message_box = st.chat_message('user')
        message_box.markdown(message.content)

# 3.State variables (good for debugging)
with right_column:
    st.text(st.session_state.message_history)
   
   
   