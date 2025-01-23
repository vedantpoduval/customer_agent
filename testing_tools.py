# The function name, type hints, and docstring are all part of the tool
# schema that's passed to the model. Defining good, descriptive schemas
# is an extension of prompt engineering and is an important part of
# getting models to perform well.
from langchain_core.tools import tool
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage
assert os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
llm = ChatVertexAI(model="gemini-1.5-flash")

@tool
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer
        b: Second integer
    """
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers.

    Args:
        a: First integer
        b: Second integer
    """
    return a * b
tools = [add, multiply]

llm_with_tools = llm.bind_tools(tools)

query = "What is 3 * 12?"

messages = [HumanMessage(query)]

print(messages)
ai_msg = llm_with_tools.invoke(messages)
print(ai_msg.tool_calls)
messages.append(ai_msg)
# final_tool = ai_msg.tool_calls[0]['name']
tool_msg = multiply.invoke(ai_msg.tool_calls)
print(tool_msg)
messages.append(tool_msg)
response = llm_with_tools.invoke(messages)
print(response.content)
# for tool_call in ai_msg.tool_calls:
#     selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
#     print(selected_tool)
#     tool_msg = selected_tool.invoke(tool_call)
#     messages.append(tool_msg)
# print(messages)
# response = llm_with_tools.invoke(messages)
# print(response.content)


# import os
# from dotenv import load_dotenv
# load_dotenv()
# from langchain_google_vertexai import ChatVertexAI
# assert os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# model = ChatVertexAI(model="gemini-1.5-flash")
# response = model.invoke("Hi I am Vedant")
# print(response)


