import dotenv
import os

dotenv.load_dotenv()

import base64

from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage, AIMessage

#初始化大模型
model = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL")
)
# 方式一 文字对话形式
# 创建一个列表，保存和大模型对话
message = [
    SystemMessage(content="你是一个编程助手")
]

print("=======================================1===========================")
message.append(HumanMessage(content="帮我写一个请求代码"))

#第一轮对话
response = model.stream(message)

ai_message = ''

for chunk in response:
    print(chunk.content, end='')
    ai_message += chunk.content

message.append(AIMessage(content=ai_message))

print("=======================================2===========================")
message.append(HumanMessage(content="改写请求代码"))
#开启第二轮对话

response = model.stream(message)

for chunk in response:
    print(chunk.content, end='')

"""
 AI大模型上下文
    多条记录里面 ,除了最后一条是用户本次需要解决,倒数第二条往前都是上下文背景
    记录所有对话的message就是大模型上下文窗口： 大概都在200k上 200k=200 *1024 个token
 AI大模型持续对话
     所有消息都放在message里面,时间一长就会超出大模型最大上下文处理的限制,就会出现记忆丢失的问题,再往下处理
     解决办法：进行上下文管理工程 做摘要提取（从对话记录中保存重要信息提取到永久记忆--文件/数据库）
     
"""


