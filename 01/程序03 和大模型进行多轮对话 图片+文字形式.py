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

messages = [
    SystemMessage(content="你是一个编程助手")
]

# 方式二 图片对话形式

# 本地图片转换为base64形式
# 1. 获取本地文件路径
pdf_path = "/Users/yiliyuan/Downloads/发票票面/广告票.pdf"

# 2. 读取二进制并转为字符串
with open(pdf_path, "rb") as f:
    image_data=f.read()
    base64_str = base64.b64encode(image_data).decode('utf-8')

print(base64_str)


user_message = HumanMessage(content=[
    {"type": "text", "text": "帮我分析这个新的需求，提取测试点"},
    {"type": "image", "mime_type": "image/pdf", "base64": base64_str},
])

messages.append(user_message)
# 第一轮对话

response = model.stream(messages)
for chunk in response:
    print(chunk.content, end='')