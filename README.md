RAG 知识库问答机器人 🤖
基于 LangChain、阿里云百炼平台和 Streamlit 构建的智能知识库问答系统。用户可以通过上传文档构建专属知识库，并基于知识库内容进行智能问答。

✨ 功能特点
📚 知识库管理：支持上传多种格式文档（TXT、PDF、Markdown 等），构建个性化知识库

🔍 智能检索：基于 RAG（检索增强生成）技术，结合向量检索与大语言模型

💬 交互式问答：通过 Streamlit 提供友好的 Web 界面，实时问答交互

🚀 云端模型：集成阿里云百炼平台的大语言模型，提供高质量回答

📊 对话历史：保存问答记录，支持上下文连续对话

🛠️ 技术栈
核心框架：LangChain

大语言模型：阿里云百炼平台（通义千问系列）

向量数据库：Chroma / FAISS

前端界面：Streamlit

编程语言：Python 3.10+

📁 项目结构
text
RAG/
├── app.py                 # Streamlit 主应用
├── rag_chain.py           # RAG 链构建逻辑
├── document_loader.py     # 文档加载与处理
├── vector_store.py        # 向量存储管理
├── requirements.txt       # 项目依赖
├── .env                   # 环境变量配置（不提交）
├── data/                  # 上传文档存储目录
├── chroma_db/             # 向量数据库存储
└── README.md              # 项目说明
