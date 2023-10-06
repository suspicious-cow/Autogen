
## AutoGen N-Agent Example
### Initial setup for the notebook to work

# *WARNING:* This will cost money to run. In my case it cost about 0.20 USD using the basic ChatGPT-4 model. It can add up real fast so watch your usage closely. 

# just show stdout not stderr messages
# %%capture --no-stderr

# uncomment to install pyautogen if you don't have it already
# %pip install pyautogen


### Import the autogen package and do agent configuration
import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# load the config list from the environment variable or file
# in my case, I have an environment variable called OAI_CONFIG_LIST
# that is set to the JSON string [{"model": "gpt-4","api_key": "<my api key>"}]
gpt4_config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

# set up other parameters as needed
gpt4_config = {
    "seed": 42,  # change the seed for different trials
    "temperature": 0,
    "config_list": gpt4_config_list,
    "request_timeout": 120,
}


### Setup the agents
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human to get started. Once the instructions are clear, assume the plan is approved.",
    code_execution_config=False,
)
engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=gpt4_config,
    human_input_mode="NEVER",
    system_message='''Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
''',
)
scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config=gpt4_config,
    human_input_mode="NEVER",
    system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code."""
)
planner = autogen.AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
''',
    llm_config=gpt4_config,
)
executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"},
)
critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    human_input_mode="NEVER",
    llm_config=gpt4_config,
)


## Assemble the agents into a group chat
groupchat = autogen.GroupChat(agents=[user_proxy, engineer, scientist, planner, executor, critic], messages=[], max_round=10)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)


### Launch the chat
user_proxy.initiate_chat(
    manager,
    message="""
find 4 papers on LLM applications from arxiv in the last week prioritizing more recent articles,give me a one sentence summary of each one.
""",
)

