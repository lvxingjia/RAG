import time

import streamlit as st

from knowledge_base import KnowledegBaseService

st.title("知识库更新")
st.text("nihao")
uploader_file=st.file_uploader(

    "请上传文件",
    type=['txt'],
    accept_multiple_files=False


)

# st.sess
if "service" not in st.session_state:
    st.session_state["service"] =KnowledegBaseService()#实例化一个上传对象

if uploader_file is not None:
        # 提取文件信息
    file_name=uploader_file.name
    file_type=uploader_file.type
    file_size=uploader_file.size/1024 #KB
    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type},大小：{file_size}"+"KB")

    text=uploader_file.getvalue().decode("utf-8")

    with st.spinner("载入进知识库中..."):
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)

