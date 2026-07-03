import dotenv
import os

dotenv.load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import create_agent
from langchain.tools import tool

#初始化大模型
model = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL")
)

system_prompt = [
    SystemMessage(content="你是一个编程助手")
]


# 定义一个给大模型调用的工具
@tool("写文件的工具", description="用于将智能体生成内容写入文件")
def write_file(file_path: str, content: str):
    """将内容写入指定路径的文件。参数: file_path(文件路径), content(写入内容)"""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"成功写入文件: {file_path}"
    except Exception as e:
        return f"写入失败: {str(e)}"


@tool("读文件的工具", description="读文件工具")
def read_file(file_path: str):
    """读取指定路径的文件内容。参数: file_path(文件路径)"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"读取失败: {str(e)}"


# 创建第一个agent智能体     给智能体配置模型
agent = create_agent(
    model=model,
    tools=[write_file, read_file],
    system_prompt=system_prompt

)

# ========第一轮对话==========
user_prompt = HumanMessage(content="""

    


""")

# 运行agent和它对话
response = agent.stream(input={
    "message": [user_prompt]
})

for chunk in response:
    print(chunk)
