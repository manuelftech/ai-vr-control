#from langchain.agents import initialize_agent, Tool
#from langchain.agents import load_tools
#from langchain.agents import AgentType
#from db.get_db import get_item_from_dynamodb
from langchain_aws import BedrockLLM
from dotenv import load_dotenv
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

def init_chatbot_v2():
    #from langchain import hub
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain.tools import Tool, tool

    logging.info("Connecting to LLM model in AWS")
    load_dotenv()

    # 1. Define your tools
    @tool
    def get_item_from_dynamodb(rut: str):
        "Use this when you need to lookup a customer by rut."
        # removing unwanted new lines or tab
        rut = rut.strip('\n').strip('\t')
        logging.info("Querying database using rut %s", rut)
        dynamodb = boto3.client("dynamodb", region_name=os.environ.get("DATABASE_AWS_REGION"))
        found_customer = dynamodb.get_item(TableName=os.environ.get("DYNAMODB_TABLE"), Key={os.environ.get("TABLE_PARTITION_KEY"):{'S':os.environ.get("TABLE_PARTITION_VALUE")}, 'rut':{'S': str(rut)}})
        logging.debug("Item found in Database for rut %s: %s", rut, found_customer)
        return found_customer['Item']

    tools = [get_item_from_dynamodb]

    # 2. Get the prompt to use for the agent
    #prompt = hub.pull("hwchase17/react")

    # 3. Create a language model (LLM)
    llm = BedrockLLM(
        credentials_profile_name="bedrock-admin", 
        model_id=os.environ.get("LLM_MODEL_ID")
    )
    # 4. Create the ReAct agent
    #agent = create_react_agent(llm, tools, prompt)
    agent = create_react_agent(llm, tools)

    # 5. Create the AgentExecutor
    react_agent = AgentExecutor(tools=tools, agent=agent, verbose=True)
    
    logging.info("Agent properly initialized in AWS")
    return react_agent
