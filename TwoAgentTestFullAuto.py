from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})

# Set human_input_mode to 'off' and max_consecutive_auto_reply to a high number for full autonomy
# These are hypothetical settings, as exact parameter names and values would depend on the actual implementation of AutoGen
user_proxy = UserProxyAgent("user_proxy", 
    code_execution_config={"work_dir": "coding"},
    human_input_mode='off', 
    max_consecutive_auto_reply=1000)

# This initiates an automated chat between the two agents to solve the task
user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")


