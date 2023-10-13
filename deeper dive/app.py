import autogen
import os

# get api key from environment variable
api_key = os.environ.get('OPENAI_API_KEY')

# set up the autogen model config 
config_list = [
    {
        'model': 'gpt-4',
        'api_key': api_key,
    }
]

llm_config = {
    'request_timeout': 600,
    'seed': 1337,
    'config_list': config_list,
    'temperature': 0,
}

assistant = autogen.AssistantAgent(
    name='assistant',
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name='user_proxy',
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get('content','').rstrip().endswith('TERMINATE'),
    code_execution_config={'work_dir':'web', use_docker: False},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved to full satisfaction. Otherwise reply CONTINUE or the reason why the task is not solved yet."""   
)

task = """
Give me a summary of this article https://www.marketwatch.com/story/inflation-is-already-racing-past-next-years-social-security-cola-93ad969e
"""

user_proxy.initiate_chat(assistant, 
    message = task
)