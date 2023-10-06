####
#Copyright (c) 2023 Rikito Ohnishi
#Released under the MIT license
#https://opensource.org/licenses/mit-license.php
####

from fastapi import FastAPI
from fastapi.responses import HTMLResponse,FileResponse
from pydantic import BaseModel

import os

# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import (
#     ChatPromptTemplate,
#     MessagesPlaceholder,
#     SystemMessagePromptTemplate,
#     HumanMessagePromptTemplate
# )
# from langchain.chains import ConversationChain
# from langchain.chat_models import ChatOpenAI
# from langchain.memory import ConversationBufferMemory
import webbrowser
template = """#Instructions :
You are an American professional English teacher.
Please chat with me under the following constraints.

#Constraints:

・I am a beginner in English.
・You can choose the topic for our conversation.
・We will take turns writing one sentence at a time.
・If you notice any grammatical errors in my sentences, please correct them and explain why you made the correction.
・If Japanese is spoken, please translate it into English and respond."""


app = FastAPI()

# ファイル取得
@app.get("/index.html", response_class=HTMLResponse)
async def html():
  return FileResponse("./web/index.html")
@app.get("/style.css")
async def style():
  return FileResponse("./web/style.css")
@app.get("/script.js")
async def script():
  return FileResponse("./web/script.js")
@app.get("/jQuery.js")
async def jQuery():
  return FileResponse("./web/code.jquery.com_jquery-3.7.1.min.js")

# 既存のOpenAI API KEYがないか確認
@app.get("/initialization")
async def init():
  if os.getenv('OPENAI_API_KEY') != None:
    return {"OpenAI_API_KYE":True}
  else:
    return {"OpenAI_API_KYE":False}

# 既存のOpenAI API KEYを登録もしくは削除
class APIKEY(BaseModel):
    key: str
@app.post("/API_KEY")
async def SetAPIKey(data:APIKEY):
  if data.key == "":
    if os.getenv('OPENAI_API_KEY') != None:
      os.environ.pop('OPENAI_API_KEY')
    return {"SetAPI":False}
  else:
    os.environ["OPENAI_API_KEY"] = data.key
    return {"SetAPI":True}


  # print("code restart")
  # st.sidebar.title('CHATGPT-EIKAIWA')
  # st.sidebar.caption('[GitHub](https://github.com/plumchloride/ChatGPT-Eikaiwa)')
  # openai_apikey = st.sidebar.text_input('OpenAI API Key', placeholder='Enter Your API key',type="password")
  # st.sidebar.text("もしくは環境変数から設定出来ます")
  # st.sidebar.code('import os \nos.environ["OPENAI_API_KEY"] = "<OpenAI_APIのトークン>"')

  # # input作成
  # st.text_input('エージェントと会話', placeholder='英語の会話を入力して下さい',on_change=ConvOpenAI(),key="inputconv")
  # # OpenAI(LangChain)起動
  # if openai_apikey != "":
  #   os.environ["OPENAI_API_KEY"] = openai_apikey
  #   openai_apikey = ""
  #   StartOpenAI()
  # elif os.getenv('OPENAI_API_KEY') != None:
  #   StartOpenAI()
  #   pass

# def StartOpenAI():
#   st.sidebar.markdown("---")
#   st.sidebar.caption("API Keyが環境変数に保存されています。削除する場合は上記テキストボックスを空のまま決定して下さい。変更する場合は再度入力し直して下さい。")
#   prompt = ChatPromptTemplate.from_messages([
#     SystemMessagePromptTemplate.from_template(template),
#     MessagesPlaceholder(variable_name="history"),
#     HumanMessagePromptTemplate.from_template("{input}")
#   ])
#   llm = ChatOpenAI(temperature=0)
#   memory = ConversationBufferMemory(return_messages=True)
#   conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

# def ConvOpenAI():
#   print(st.session_state.inputconv)

# ブラウザを開く（不要なら削除）
# webbrowser.open("http://127.0.0.1:8000", new=0, autoraise=True)