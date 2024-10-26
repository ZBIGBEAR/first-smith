import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
)
from langchain_experimental.utilities import PythonREPL
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_openai import ChatOpenAI

os.environ["QIANFAN_AK"] = "82VeQXXdQzTy9IOak9GQhxoG"
os.environ["QIANFAN_SK"] = "81ft0wqmmDHl9tdUExlVDAcfFMv2dc1O"


template = """编写一些Python代码来解决用户的问题。

只返回Markdown格式的Python代码，例如：

```python
....
```"""
prompt = ChatPromptTemplate.from_messages([("system", template), ("human", "{input}")])

# model = ChatOpenAI()
model = QianfanChatEndpoint(streaming=True,model="ERNIE-Bot",)

def _sanitize_output(text: str):
    _, after = text.split("```python")
    return after.split("```")[0]

chain = prompt | model | StrOutputParser() | _sanitize_output | PythonREPL().run

chain.invoke({"input": "2加2等于多少"})

