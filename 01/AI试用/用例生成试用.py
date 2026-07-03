import dotenv
import glob
import os

dotenv.load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import create_agent
from langchain.tools import tool

from pydantic import BaseModel, Field, field_validator

# 初始化大模型
model = ChatOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL")
)

# 创建一个agent并且配置模型

agent = create_agent(
    model=model,
    system_prompt=f"""
        你是一位有10年经验的资深软件测试工程师，精通测试需求分析，根据用户提交的需求或者是文档和图片截图,以“功能正常+边界+异常”为主线思维指导生成测试用例。
        样本示例：
        用户输入：
        需求文档：
        功能背景：Standard Void/Reverse methods in Ventures：提供标准的 by国家 by单据的 void 解决方案。第一期覆盖 ARM 模块。
        主流程
        1）用户选择一张已生效的 ARM 单据，执行 Void 操作。
        2）系统校验单据状态是否允许 Void。
        3）校验通过后，系统在数据库层面对该单据进行 Void 打标（非物理删除）。
        4）系统生成/更新该单据的 PDF，并在 PDF 上添加 Void 水印。
        5）操作成功，提示用户 Void 完成。
        异常流程
        1、 单据状态不允许 Void（如已 Void、已核销）：提示“当前状态无法执行 Void”。
        2、无操作权限：提示“权限不足”。
        3、打标或生成 PDF 失败：提示“Void 操作失败，请重试或联系管理员”，数据回滚。
        业务规则
        1、核心原则：Void 是逻辑打标，严禁物理删除原始记录。
        2、数据层：Void 后，单据状态字段更新为 VOIDED，保留原始创建时间和操作人。
        3、展示层：Void 后的 PDF 必须包含明显的 VOID 水印，且水印不可被轻易去除。
        4、范围：第一期仅支持 ARM 模块单据。
        5、不可逆：Void 操作不可撤销（除非通过数据订正流程）。
        **约束规范：**
        1. 生成的测试点不要有重复内容
        2. 用例编号需遵循 TC_模块_功能_序号 的格式
        3. 必须覆盖主流程、异常流程和关键业务规则
        4. 关注数据完整性和事务回滚场景

    """,
    tools=[],
)
# 读需求文档

file_path = "/Users/yiliyuan/Downloads/测试/发票需求产品文档"

# 2. 获取文件夹下所有的 .md 文件
md_files = glob.glob(os.path.join(file_path, "*.md"))
merged_content = " "
# 3. 检查是否找到了文件
if not md_files:
    print("❌ 未找到任何 .md 文件，请检查文件夹路径是否正确！")
else:
    print(f"✅ 成功找到 {len(md_files)} 个需求文档，开始读取...")

    # 4. 循环读取并拼接内容
    all_docs_content = []
    for file_path in md_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # 加上文件名作为分隔，防止 AI 混淆不同文档的内容
                all_docs_content.append(f"===== 需求文档: {os.path.basename(file_path)} =====\n{content}\n")
        except Exception as e:
            print(f"⚠️ 读取 {file_path} 失败: {e}")

        # 5. 将所有文档内容用换行符拼接成一个完整的字符串
        merged_content = "\n\n".join(all_docs_content)

user_prompt = HumanMessage(content=merged_content)

response = agent.invoke({
    "message": [user_prompt]
})

print(response)


