# 这里是知识库
from sqlalchemy.testing.suite.test_reflection import metadata
from sympy.multipledispatch.dispatcher import source

import config_data as config
import os
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import dashscope, DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5( md5_str:str ):#检查MD5字符串是否被处理

    # md5哈希算法；无论文本内容多大，都可以计算成32位16进制字符，对于知识库储存要求高效快速
    #使用md5可以快速查询当前文本是否在知识库
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding='utf-8').close()

        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():
            line=line.strip()
            if line == md5_str:
                return True

    return False

def save_md5(md5_str:str):
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')



def get_string_md5(input_str: str , encoding='utf-8'):#讲字符川还原为bytes数组
    str_bytes=input_str.encode(encoding=encoding)
#    创建md5对象
    md5_obj=hashlib.md5()#得到md5对象
    md5_obj.update(str_bytes)#更新md5内容
    md5_hex= md5_obj.hexdigest()
    return md5_hex


class KnowledegBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True)#如果文件不存在就创建，反之跳过
        self.chroma=Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory

        )
        self.spliter=RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,       #分割后文本段最大长度
            chunk_overlap=config.chunk_overlap,         #连续文本段之间的字符重叠数量
            separators=config.separators,       #自然段落划分的符号
            length_function=len,        #python自带长度统计

        )

    def upload_by_str(self,data:str,filename):

        #先将传入字符串向量化，存入向量数据库
        md5_hex=get_string_md5(data)
        if check_md5(md5_hex):
            return "跳过 内容已在知识库中"
        if len(data)>config.max_split_char_number:
            knowledge_chunks:list[str]=self.spliter.split_text(data)
        else:
            knowledge_chunks=[data]

        metadata={
            "source":filename,
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"小吕",
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )
        save_md5((md5_hex))
        return "[成功] 数据上传到知识库"

if __name__=='__main__':
    service=KnowledegBaseService()
    r=service.upload_by_str("周杰伦",filename="testfile")
    print(r)


