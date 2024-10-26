import os,sqlparse

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

os.environ["QIANFAN_AK"] = "82VeQXXdQzTy9IOak9GQhxoG"
os.environ["QIANFAN_SK"] = "81ft0wqmmDHl9tdUExlVDAcfFMv2dc1O"

# 这个prompt将数据库schema和要求以及问题交给大模型，让大模型生成sql
template = """根据下面的表模式，编写一个SQL查询来回答用户的问题：
{schema}

问题：{question}
注意：
1.你只需要返回可执行的sql语句，不要返回其他内容
2.sql语句不要用引号包裹
"""
prompt = ChatPromptTemplate.from_template(template)
# 链接数据库
db = SQLDatabase.from_uri("mysql+pymysql://baiduziyuan:baiduziyuan20240313@124.222.247.48:3306/qingshiliuming?charset=utf8mb4")

# 获取数据库schema
def get_schema(_):
    return db.get_table_info()

# 解析大模型返回的内容，提取sql
def parse_sql(query):
    return query.split("```sql")[1].split("```")[0]

# 执行sql
def run_query(sql):
    return db.run(sql)

# model = ChatOpenAI()
model = QianfanChatEndpoint(streaming=True,model="ERNIE-Bot",)

sql_response = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | model.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

# 将问题、sql语句以及查询结果交给大模型，让大模型生成一个自然语言回答的结果
template1 = """根据下面的表模式，问题，SQL查询和SQL响应，编写一个自然语言回答：
{schema}

问题：{question}
SQL查询：{query}
SQL响应：{response}"""
prompt_response = ChatPromptTemplate.from_template(template1)

full_chain = (
    RunnablePassthrough.assign(query=sql_response).assign(
        schema=get_schema,
        response=lambda x: run_query(parse_sql(x["query"])),
    )
    | prompt_response
    | model
    | StrOutputParser()
)

# print(full_chain.invoke({"question": "有多少人？"}))
# print(full_chain.invoke({"question": "根据数据库中的记录，秦始皇又叫什么？"}))
# 流式获取大模型返回的结果
try:
    for chunk in full_chain.stream({"question": "根据数据库中的记录，秦始皇又叫什么？"}):
        print(chunk, end="", flush=True)
except TypeError as e:
    print("")