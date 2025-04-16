from openai import OpenAI
import streamlit as st
from fewshot_data import few_shot_data

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/yangdorodong/chatbot/edit/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("MBTaIk")
st.caption("원하는 MBTI 스타일을 말해봐!")

system_prompt = f"""너는 원하는 MBTI에 맞게 고민상담을 해주는 챗봇이야.
이 데이터는 16가지 mbti의 특징을 보여줘:
{few_shot_data}
"""

if "messages" not in st.session_state:
    
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "원하는 MBTI가 있어요?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
