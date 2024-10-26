import os

from langchain.tools import DuckDuckGoSearchRun
# from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import QianfanChatEndpoint

os.environ["QIANFAN_AK"] = "82VeQXXdQzTy9IOak9GQhxoG"
os.environ["QIANFAN_SK"] = "81ft0wqmmDHl9tdUExlVDAcfFMv2dc1O"

search = DuckDuckGoSearchRun()

template = """将以下用户输入转换为搜索引擎的搜索查询：

{input}"""
prompt = ChatPromptTemplate.from_template(template)

model = QianfanChatEndpoint(streaming=True,model="ERNIE-Bot",)

chain = prompt | model | StrOutputParser() | search| StrOutputParser()

try:
    for chunk in chain.stream({"input": "今天上海有什么演唱会？"}):
        print(chunk, end="", flush=True)
except TypeError as e:
    print("")