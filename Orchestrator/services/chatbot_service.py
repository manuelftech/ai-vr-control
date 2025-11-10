#from langchain.agents import initialize_agent, Tool
#from langchain.agents import load_tools
#from langchain.agents import AgentType
#from db.get_db import get_item_from_dynamodb
from langchain_aws import BedrockLLM

import logging
import boto3
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# def init_chatbot():
#     logging.info("Connecting to LLM model in AWS")
#     load_dotenv()

#     model_parameter = {"temperature": float(os.environ.get("TEMPERATURE")), "top_p": float(os.environ.get("TOP_P")), "max_tokens_to_sample": int(os.environ.get("MAX_TOKENS_TO_SAMPLE"))}
#     boto3_bedrock = boto3.client(service_name='bedrock-runtime', region_name=os.environ.get("LLM_AWS_REGION"))
#     llm = Bedrock(model_id=os.environ.get("LLM_MODEL_ID"), client=boto3_bedrock, model_kwargs=model_parameter, region_name=os.environ.get("LLM_AWS_REGION"))

#     react_agent_llm = Bedrock(model_id=os.environ.get("LLM_MODEL_ID"), model_kwargs=model_parameter, region_name=os.environ.get("LLM_AWS_REGION"))
#     tools = load_tools(["wikipedia"], llm=react_agent_llm)
#     tools.append(Tool.from_function(
#             name="get_item_from_dynamodb",
#             func=get_item_from_dynamodb,
#             description="Use this when you need to lookup a customer by rut."
#         ))

#     react_agent = initialize_agent(tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
#     logging.info("Agent properly initialized in AWS")
#     return react_agent

