"""For basic init and call"""
import os

from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.language_models.chat_models import HumanMessage

# os.environ["QIANFAN_AK"] = "qpC1oWfh7jCRFErNsbr0amk2"
# os.environ["QIANFAN_SK"] = "VNe8VOmzDwbHoi5dePommVorj1vSZTy6"

os.environ["QIANFAN_AK"] = "82VeQXXdQzTy9IOak9GQhxoG"
os.environ["QIANFAN_SK"] = "81ft0wqmmDHl9tdUExlVDAcfFMv2dc1O"

chat = QianfanChatEndpoint(streaming=True,model="ERNIE-Bot",)
messages = [HumanMessage(content="请问1+1等于几？为什么？")]
# result = chat.invoke(messages,top_p=0.4, temperature= 0.1, penalty_score= 1)
# print(result)
try:
    for chunk in chat.stream(messages):
        print(chunk.content, end="", flush=True)
except TypeError as e:
    print("")