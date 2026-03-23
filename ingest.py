import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. 加载所有 PDF 文档
docs = []
pdf_folder = "./docs"
for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(pdf_folder, file))
        docs.extend(loader.load())  # loader.load() 返回 Document 对象列表

print(f"加载了 {len(docs)} 个文档页")

# 2. 文本分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # 每块最大字符数
    chunk_overlap=50,      # 块之间的重叠字符数，保持上下文连贯
    separators=["\n\n", "\n", "。", "！", "？", "，", "、", " "]  # 中文分隔符
)
chunks = text_splitter.split_documents(docs)

print(f"分割成 {len(chunks)} 个文本块")
# 可打印一个示例看看
print(chunks[0].page_content)