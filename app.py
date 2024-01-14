
import streamlit as st
import openai
#from openai import OpenAI
from PIL import Image

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OPENAI_API_KEY.openai_api_key
# client = OpenAI(
# api_key=st.secrets.OPENAI_API_KEY.openai_api_key,)

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
     )
    # response = client.chat.completions.create(model="gpt-3.5-turbo",
    # messages=messages)  

    bot_message = response["choices"][0]["message"]
    # bot_message = response.choices[0].message
    messages.append(bot_message)
    # print(bot_message)
    
    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("プランマイスターの館")
st.write("ChatGPTが宿泊プラン作成のマイスターとしてプラン文章を作成してくれます")
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("ホテルの支配人")
    st.image("master.jpg", use_column_width=True)
with col2:
    st.subheader("ギャル")
    st.image("master.jpg", use_column_width=True)
with col3:
    st.subheader("旅館の女将")
    st.image("master.jpg", use_column_width=True)
    
# image = Image.open('master.jpg')
# st.image(image, caption='※プランマスターイメージ｜AI生成',use_column_width=False)

user_input = st.text_input("ホテルの特徴や作りたいプランの内容を入力してください。立地や食事の有無等", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🗨️🙂"
        if message["role"]=="assistant":
            speaker="🗨️😘"

        st.write(speaker + ": " + message["content"])
