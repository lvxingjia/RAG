from xml.dom.minidom import Document

import langchain_community.embeddings
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from sqlalchemy.testing.suite.test_reflection import metadata

import config_data as config
import vectors_store
from file_history_store import get_history
from vectors_store import VectorstoreService
from langchain_core.prompts import ChatPromptTemplate, format_document, MessagesPlaceholder


def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt

class RagService(object):
    def __init__(self):
        self.vector_servcie=VectorstoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model)
        )
        self.prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的参考资料为主，简介专业地回答用户问题。参考资料：{context}。"),
                ("system","并且我提供用户对话历史记录如下："),
                MessagesPlaceholder("history"),
                ("user","请回答用户提问:{input}")


            ]


        )
        self.chat_model=ChatTongyi(model=config.chat_model)
        self.chain=self.__get_chain()


    def __get_chain(self):
        retriever = self.vector_servcie.get_retriver()

        def format_document(docs:list[Document]):
            if not docs:
                return  "无相关参考资料"
            formatted_str=""
            for doc in docs:
                formatted_str+= f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return formatted_str

        def temp1(value:dict)->str:
            return value["input"]

        def temp2(value):
            new_value={}
            new_value["input"]=value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain=(

            {
                "input":RunnablePassthrough(),
                "context":RunnableLambda(temp1)|retriever | format_document

            }|RunnableLambda(temp2)|self.prompt_template| self.chat_model |StrOutputParser()
            #}|self.prompt_template|print_prompt| self.chat_model |StrOutputParser()

        )
        # pass

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return  conversation_chain



if __name__=="__main__":

    res=RagService().chain.invoke({"input":"我上次的问题是什么"},session_config)
    print(res)