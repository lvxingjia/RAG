md5_path ="./md5.text"
#向量库
collection_name = "RAG"
persist_directory = "./chroma_db"
#


#模型配置
embedding_model="text-embedding-v4"
chat_model="qwen3-max"

#文本分割器
chunk_size=1000
chunk_overlap=100
separators=["\n\n","\n",".","!","?","。","！","？","，"," ",""]
max_split_char_number=1000


#向量检索
similarity_threshold=1

session_config ={
        "configurable":{
            "session_id":"user_001",
        }
    }