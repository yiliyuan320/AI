import dotenv
import os

dotenv.load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import create_agent
from langchain.tools import tool
# 进行数据类型校验的库pydantic 中的BaseModel类 若类型不符合报错，还可以进行JSON格式的转换
#field_validator可以对字段的值进行判断，Field对值进行默认值和必填等约束 ...


from pydantic import BaseModel, Field,field_validator

#初始化大模型
model = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL")
)

# 定义模型输出内容的格式 大模型生成的本质为字符串，转化为python中可操作的格式JSON

# ===================设置系统提示词===================
system_prompt = SystemMessage(content=""""
   
""")

user_prompt = HumanMessage(content=""""

""")


#===================定义期望的数据格式===================

class TestCase(BaseModel):
    """
    定义生成的数据类型类
    在类里面定义生成的用例数据需要哪些字段
    """
    id: int = Field(..., description="用例编号")
    case_name: str = Field(..., description="用例名称")
    test_data: str = Field(..., description="测试数据")
    test_step: str = Field(..., description="测试步骤")

class CaseModel(BaseModel):
    """
    定义输出的数据模型类
    """
    case_list: list[TestCase] = Field(..., description="用例列表")
    case_count: int = Field(..., description="用例数量")
    name:str =Field(...,description="测试的功能")


# 用来进行绑定用例输出的类型格式 但是这种方法生成的用例只能生成一个
model_bit_output = model.with_structured_output(CaseModel)

message = [system_prompt, user_prompt]

response = model_bit_output.invoke(message)


# 将pydantic模型转换为python字典 方便在python里面处理数据
print(response.model_dump())
# 将pydantic模型转换为JSON字符串
print(response.model_dump_json())

response = model.invoke(message)
