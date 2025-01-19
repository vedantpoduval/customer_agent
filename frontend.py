import streamlit as st

st.set_page_config(page_title="flower shop chatbot",page_icon="🌻",layout="wide")

if 'message_history' not in st.session_state:
    st.session_state.message_history = [{'content' : "Hey , I am the flower shop chatbot how can I help",'type':'assistant'}]


left_column,main_column,right_column = st.columns([1,2,1])

# 1.Buttons for chat - Clear button(first column)
with left_column:
    if st.button('Clear Chat'):
        st.session_state.message_history = []
 
# 2.Chat history and input        
with main_column:
    user_input = st.chat_input('Enter your chat')
    if user_input:
        # st.text(user_input)
        st.session_state.message_history.append({'content': user_input,'type':'user'})
    for message in reversed(st.session_state.message_history):
        message_box = st.chat_message(message['type'])
        message_box.markdown(message['content'])

# 3.State variables (good for debugging)
with right_column:
    st.text(st.session_state.message_history)
   
   
   