import os

from langchain.tools import DuckDuckGoSearchRun
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import QianfanChatEndpoint

os.environ["QIANFAN_AK"] = "82VeQXXdQzTy9IOak9GQhxoG"
os.environ["QIANFAN_SK"] = "81ft0wqmmDHl9tdUExlVDAcfFMv2dc1O"

search = DuckDuckGoSearchRun()

template = """将以下用户输入转换为搜索引擎的搜索查询：

{input}"""
prompt = ChatPromptTemplate.from_template(template)

# model = ChatOpenAI()
model = QianfanChatEndpoint(streaming=True,model="ERNIE-Bot",)

chain = prompt | model | StrOutputParser()|search

print(chain.invoke({"input": "我想弄清楚今晚有哪些比赛"}))