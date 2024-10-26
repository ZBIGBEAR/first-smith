# from langchain.agents import initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# from langchain.llms import OpenAI
import requests
from bs4 import BeautifulSoup
import os
import sys
from langchain_community.chat_models import QianfanChatEndpoint
from langchain.chains import ConversationChain


os.environ["QIANFAN_AK"] = "82VeQXXdQzTy9IOak9GQhxoG"
os.environ["QIANFAN_SK"] = "81ft0wqmmDHl9tdUExlVDAcfFMv2dc1O"
model = QianfanChatEndpoint(streaming=True, model="ERNIE-Bot", )
# 构建对话链条
conversation = ConversationChain(llm=model)

# 创建网页抓取函数
def fetch_website_content(url):
    # print('开始获取网页内容...')
    response = requests.get(url)
    response.raise_for_status()  # 确保请求成功
    soup = BeautifulSoup(response.text, 'html.parser')
    # print('已获取完网页内容')
    return soup.get_text()

# 创建总结函数
def summarize_content(content):
    # print('开始总结...')
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="请总结以下内容：\n{text}\n总结："
    )
    if(len(content) > 5*1024):
        content = content[:5*1024]
    chain = LLMChain(llm=model, prompt=prompt_template)
    summary = chain.run({"text": content})
    # print('总结完成')
    return summary


def ask_question_about_page(question,content):
    template = """
    网页内容如下:
    {content}

    用户问题: {question}
    请基于网页内容回答问题。
    """
    prompt = PromptTemplate.from_template(template)
    response = conversation.predict(input=prompt.format(content=content, question=question))
    return response

# 主函数
def summarize_website(url,question):
    content = fetch_website_content(url)
    if (len(content) > 5 * 1024):
        content = content[:5 * 1024]
    # summary = summarize_content(content)
    summary = ask_question_about_page(question,content)
    return summary


# 示例用法
if __name__ == "__main__":
    # url = input("请输入网址：")
    url = sys.argv[1]
    question = sys.argv[2]
    summary = summarize_website(url,question)
    print(summary)
