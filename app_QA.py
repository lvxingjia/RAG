# import time
# import streamlit as st
# from rag import RagService
# import config_data as config
#
# # ==================== 页面配置 ====================
# st.set_page_config(
#     page_title="知识库问答",
#     page_icon="",  # 移除 emoji
#     layout="wide",
#     initial_sidebar_state="collapsed"  # 侧边栏默认收起，点击可展开
# )
#
# # ==================== 自定义CSS（简洁风格，无居中） ====================
# st.markdown("""
# <style>
#     /* 整体背景与字体 */
#     .stApp {
#         background: linear-gradient(135deg, #f5f7fa 0%, #eef2f6 100%);
#         font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
#     }
#
#     /* 主内容容器 - 增加内边距与圆角卡片效果 */
#     .main .block-container {
#         max-width: 800px;
#         padding: 2rem 1rem 8rem 1rem;
#         background-color: rgba(255,255,255,0.9);
#         backdrop-filter: blur(2px);
#         border-radius: 24px;
#         margin: 1rem auto;
#         box-shadow: 0 8px 20px rgba(0,0,0,0.05);
#     }
#
#     /* 自定义滚动条 */
#     ::-webkit-scrollbar {
#         width: 6px;
#     }
#     ::-webkit-scrollbar-track {
#         background: #f1f1f1;
#         border-radius: 10px;
#     }
#     ::-webkit-scrollbar-thumb {
#         background: #c1c1c1;
#         border-radius: 10px;
#     }
#
#     /* 消息气泡通用样式 */
#     .stChatMessage {
#         border-radius: 20px !important;
#         padding: 12px 18px !important;
#         margin-bottom: 20px !important;
#         transition: all 0.2s ease;
#         font-size: 0.95rem;
#         line-height: 1.5;
#         box-shadow: 0 1px 2px rgba(0,0,0,0.03);
#     }
#
#     /* 用户消息：右对齐，渐变背景 */
#     [data-testid="stChatMessage"][data-role="user"] {
#         background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%) !important;
#         border-bottom-right-radius: 4px !important;
#         margin-left: auto !important;
#         width: fit-content !important;
#         max-width: 80% !important;
#         color: #1e293b !important;
#         border: none !important;
#     }
#
#     /* 助手消息：左对齐，白色带微妙阴影 */
#     [data-testid="stChatMessage"][data-role="assistant"] {
#         background-color: #ffffff !important;
#         border: 1px solid #e2e8f0 !important;
#         border-bottom-left-radius: 4px !important;
#         margin-right: auto !important;
#         width: fit-content !important;
#         max-width: 80% !important;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.02), 0 1px 2px rgba(0,0,0,0.05);
#     }
#
#     /* 输入框区域美化 */
#     .stChatInput {
#         border-radius: 28px !important;
#         border: 1px solid #e2e8f0 !important;
#         background: #ffffff !important;
#         padding: 8px 20px !important;
#         box-shadow: 0 2px 6px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.03) !important;
#     }
#     .stChatInput:focus-within {
#         border-color: #6366f1 !important;
#         box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
#     }
#
#     /* 侧边栏精致化 */
#     [data-testid="stSidebar"] {
#         background: #ffffff;
#         border-right: 1px solid #eef2f6;
#         box-shadow: 2px 0 10px rgba(0,0,0,0.02);
#         padding-top: 2rem;
#     }
#
#     /* 按钮圆润 */
#     .stButton button {
#         border-radius: 40px;
#         background: #f8fafc;
#         border: 1px solid #e2e8f0;
#         transition: all 0.2s;
#     }
#     .stButton button:hover {
#         background: #f1f5f9;
#         border-color: #cbd5e1;
#         transform: translateY(-1px);
#     }
#
#     /* 标题样式 */
#     .stTitle {
#         font-weight: 600;
#         background: linear-gradient(135deg, #1e293b, #334155);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.5rem;
#     }
# </style>
# """, unsafe_allow_html=True)
#
# # ==================== 初始化服务 ====================
# if "rag" not in st.session_state:
#     st.session_state["rag"] = RagService()
#
# if "message" not in st.session_state:
#     st.session_state["message"] = [
#         {"role": "assistant", "content": "你好，有什么可以帮助你的？"}
#     ]
#
# # ==================== 侧边栏 ====================
# with st.sidebar:
#     st.markdown("对话设置")
#     if st.button("清空对话", use_container_width=True):
#         st.session_state["message"] = [
#             {"role": "assistant", "content": "对话已清空，请问有什么需要帮助的？"}
#         ]
#         st.rerun()
#     st.divider()
#     st.caption("Powered by Streamlit")
#
# # ==================== 主界面 ====================
# st.title("知识库问答")
#
# # 显示历史消息
# for message in st.session_state["message"]:
#     role = message["role"]
#     content = message["content"]
#     with st.chat_message(role):
#         st.markdown(content)
#
# # 用户输入
# prompt = st.chat_input(placeholder="输入你的问题...")
#
# if prompt:
#     # 显示用户消息
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state["message"].append({"role": "user", "content": prompt})
#
#     # 获取AI回复（流式）
#     ai_res_list = []
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         with st.spinner("思考中..."):
#             time.sleep(0.3)
#             res_stream = st.session_state["rag"].chain.stream(
#                 {"input": prompt},
#                 config.session_config
#             )
#
#         full_response = ""
#         for chunk in res_stream:
#             full_response += chunk
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)
#
#     st.session_state["message"].append({"role": "assistant", "content": full_response})

import time
from rag import RagService
import streamlit as st
import config_data as config

#设置一个标题
st.title("知识库问答机器人")
st.divider()
if "rag" not in st.session_state:
    st.session_state["rag"] =RagService()

if "message" not in st.session_state:

    st.session_state["message"] = [{"role":"assistant","content":"你好有什么能帮助你"}]


for message in st.session_state["message"]:

    st.chat_message(message["role"]).write(message["content"])

#页面最下方用户输入栏
prompt = st.chat_input(
)

if prompt:
    #在页面输出用户提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})


    ai_res_list = []
    with st.spinner("AI思考中..."):
        time.sleep(1)
        res_stream=st.session_state["rag"].chain.stream({"input":prompt},config.session_config)



        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk


        st.chat_message("assistant").write_stream(capture(res_stream,ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})