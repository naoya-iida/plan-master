
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
        # {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
        {"role": "system", "content": ""}
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
st.title("プラン作り大好き族の館")
st.write("プラン作りが大好きな3人がそれぞれの特徴に合わせてプランを作ります")

 # ラジオボタンの作成
selected_option = st.radio("誰にお願いしますか？", ["ホテルの支配人", "ギャル", "旅館の女将"])
selected_optioncall = ""  # selected_optioncall を初期化
#　if selected_option:

if selected_option == "ホテルの支配人":
    chatbot_setting = """あなたはホテルの宿泊プラン向け文章を作成するのが得意です。
    ホテルの支配人のようなビジネス文章。わかりやすい箇条書きが中心。
    多くの人が予約したくなるような宿泊プランの文章を書いてください。
    立地や食事の条件など、項目ごとに分けてわかりやすく書いてください。
    料金は書かないでください
    予約方法は書かないでください"""
    selected_optioncall = "「お任せください。ホテルの特徴や立地を教えて頂ければ適切な文章を作成致します」"
elif selected_option == "ギャル":
    chatbot_setting = """あなたはホテルの宿泊プラン向け文章を作成するのが得意です。
    ギャルのようなフレンドリーな口語体。敬語は使わない。
    多くの人が予約したくなるような宿泊プランの文章を書いてください。
    立地や食事の条件など、項目ごとに分けてわかりやすく書いてください。
    料金は書かないでください
    予約方法は書かないでください"""
    selected_optioncall = "「よーし！　がんばってみんなのバイブスぶち上がるプラン作っちゃうよー☆」"
elif selected_option == "旅館の女将":
    chatbot_setting = """あなたは旅館の宿泊プラン向け文章を作成するのが得意です。
    旅館の女将のような温かみのある落ち着いた文章。
    多くの人が予約したくなるような宿泊プランの文章を書いてください。
    立地や食事の条件など、項目ごとに分けてわかりやすく書いてください。
    料金は書かないでください
    予約方法は書かないでください"""
    selected_optioncall = "「あなたの旅館の情報をいただければ、上質な滞在をお届けできるプランを作成してみますね♪」"

st.write(f"プラン作りが大好きな　{selected_option}が　しょうぶを　しかけてきた！  \n{selected_optioncall}")
st.session_state["messages"][0]["content"] = chatbot_setting  # chatbot_settingを更新

# 選択されたオプションを表示
# if selected_option:
# st.write(f"You selected: {selected_option}")

#　イメージ画像の表示
col1, col2, col3 = st.columns(3)
with col1:
    # st.subheader("ホテルの支配人")
    st.image("hotelgm.jpg", use_column_width=True)
with col2:
    # st.subheader("ギャル")
    st.image("gal.jpg", use_column_width=True)
with col3:
    # st.subheader("旅館の女将")
    st.image("okami.jpg", use_column_width=True)

user_input = st.text_input("ホテルの特徴や作りたいプランの内容や条件を入力してください。\n立地や食事の有無、周辺の観光地等。箇条書きがおすすめ", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🗨️🙂"
        if message["role"]=="assistant":
            speaker="🗨️😘"

        st.write(speaker + ": " + message["content"])
