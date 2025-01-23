from langgraph.graph import StateGraph, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage,HumanMessage
from tools import querying_knowledge_base,search_for_product_reccommendations
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from typing import List, Dict, Any
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage


import os
from dotenv import load_dotenv
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
assert os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
prompt = """#Purpose

You are a customer service chatbot for a flower shop company.You can help the customer achieve the goals listed below.

#Goals
1.Answer questions the user might have relating to services offered.
2.Recommend products to the user based on their preferences.

#Tone
Helpful and friendly.YOU MUST USE flower related puns or genz emojis to keep things lighthearted.

"""

tools = [querying_knowledge_base,search_for_product_reccommendations]
chat_template = ChatPromptTemplate(
    [('system',prompt),
     ('placeholder',"{messages}")]
)

llm = ChatVertexAI(model="gemini-1.5-flash")

output_parser = StrOutputParser()

chain = chat_template | llm.bind_tools(tools) | output_parser
def call_agent(message_state:MessagesState):
    response = chain.invoke(message_state)
    return{
        'messages':[AIMessage(content = response)]
    }

def is_there_tools_calls(state:MessagesState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'tool_node'
    else:
        return '__end__'
graph = StateGraph(MessagesState)

tool_node = ToolNode(tools=tools)

graph.add_node('agent',call_agent)
graph.add_node('tool_node',tool_node)
graph.add_conditional_edges("agent",is_there_tools_calls)
graph.add_edge('tool_node','agent')

graph.add_edge('agent','__end__')  #This is the connection of the graph when we put __end__

graph.set_entry_point('agent')

app = graph.compile()


