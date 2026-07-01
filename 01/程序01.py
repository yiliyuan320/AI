import  os
import dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


# 将.env文件加载到环境变量里面
dotenv.load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model


base_url =os.getenv("BASE_URL")

# 创建大模型调用对象

model = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL")
)
# 和大模型进行对话

# prompt 提示词格式  1、设定角色后带入上下文直接进行文本提问 2、字典形式设定提问 3、langchain规范格式

# 方法一 流式(一个一个返回) 大模型实时生成数据返回

response_1 = model.stream("你是一个测试工程师，生成测试用例的规范")

# 字典形式设定提问
response_2 = [
    # 系统角色(提示词)：设定角色或者背景描述
    {"role":"system","content":"你是一个测试工程师"},
    # 用户(提示词)：提出的问题
    {"role":"user","content":"生成测试用例的规范"}
]

# langchain规范格式
Message = [
    SystemMessage(content="你是一个测试工程师"),
    HumanMessage(content="生成测试用例的规范"),
    AIMessage(content="生成测试用例的规范")
]

for chunk in response_1:
    # content 属性里才是模型生成的文字
    print(chunk.content, end="", flush=True)


# 方法二 大模型全部生成后统一返回

response_3 =model.invoke("今天的日期是多少")
print(response_3)




