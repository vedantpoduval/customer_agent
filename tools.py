from langchain_core.tools import tool
from vector_store import FlowerShopVector
from typing import List,Dict
vector_store = FlowerShopVector()

@tool
def querying_knowledge_base(query:str) -> List[Dict[str,str]]:
    """
    Looks up information in the knowledge base to help with answering customer questions and getting information on business processes.

    Args:
        query (str): Question to ask the knowledge base

    Returns:
        List[dict[str,str]]: Potentially relevant question and answer pairs from the knowledge base
    """
    
    return vector_store.query_faqs(query=query)


@tool
def search_for_product_reccommendations(description:str):
    """
    Looks up information in the knowledge base to help with product recommendations for customers.For example:
    
    "Boquets suitable for birthdays, maybe with red flowers"
    "A large boquet for a wedding"
    "A cheap boquet with wildflowers"

    Args:
        query (str): Description of product features

    Returns:
        List[dict[str,str]]: Potentially relevant products
    """
    return vector_store.query_inventories(query=description)
# from langchain_core.tools import Tool
# from vector_store import FlowerShopVector
# from typing import List, Dict
# from pydantic import BaseModel, Field

# vector_store = FlowerShopVector()

# class QueryKnowledgeBaseSchema(BaseModel):
#     """Schema for querying the knowledge base."""
#     query: str = Field(..., description="Question to ask the knowledge base.")

# def querying_knowledge_base_tool(query: str) -> List[Dict[str, str]]:
#     """
#     Looks up information in the knowledge base to help with answering customer questions and getting information on business processes.

#     Args:
#         query (str): Question to ask the knowledge base

#     Returns:
#         List[dict[str,str]]: Potentially relevant question and answer pairs from the knowledge base
#     """
#     return vector_store.query_faqs(query=query)


# querying_knowledge_base = Tool(
#     name="querying_knowledge_base",
#     func=querying_knowledge_base_tool,
#     description="Looks up information in the knowledge base to help with answering customer questions and getting information on business processes.",
#     args_schema=QueryKnowledgeBaseSchema
# )


# class SearchProductRecommendationsSchema(BaseModel):
#     """Schema for searching for product recommendations."""
#     description: str = Field(..., description="Description of product features.")


# def search_for_product_reccommendations_tool(description: str) -> List[Dict[str, str]]:
#     """
#     Looks up information in the knowledge base to help with product recommendations for customers.For example:

#     "Boquets suitable for birthdays, maybe with red flowers"
#     "A large boquet for a wedding"
#     "A cheap boquet with wildflowers"

#     Args:
#         query (str): Description of product features

#     Returns:
#         List[dict[str,str]]: Potentially relevant products
#     """
#     return vector_store.query_inventories(query=description)



# search_for_product_reccommendations = Tool(
#     name="search_for_product_reccommendations",
#     func=search_for_product_reccommendations_tool,
#     description="Looks up information in the knowledge base to help with product recommendations for customers.",
#     args_schema=SearchProductRecommendationsSchema
# )