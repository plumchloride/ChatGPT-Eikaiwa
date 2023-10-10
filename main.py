####
#Copyright (c) 2023 Rikito Ohnishi
#Released under the MIT license
#https://opensource.org/licenses/mit-license.php
####

from fastapi import FastAPI
from fastapi.responses import HTMLResponse,FileResponse,JSONResponse
from pydantic import BaseModel
from openai import error

import os

from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
import webbrowser



app = FastAPI()


class EIKAIWA_ChatGPT():
  wakeup_flag = False
  template = """
You are an American professional English teacher named Amelie.
Please chat with me under the following constraints.
・I am a beginner in English.
・You can choose the topic for our conversation.
・We will take turns writing one sentence at a time.
・If you notice any grammatical errors in my sentences, please correct them and explain why you made the correction.
・If you notice that it is inappropriate colloquially in my sentences, please correct them and explain why you made the correction.
・If Japanese is spoken, please translate it into English and respond."""
  def wakeup(self):
      prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(self.template),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
      ])
      llm = ChatOpenAI(temperature=0)
      memory = ConversationBufferMemory(return_messages=True)
      self.conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
      self.wakeup_flag = True

chat_gpt = EIKAIWA_ChatGPT()

# ファイル取得
@app.get("/index.html", response_class=HTMLResponse)
async def html():
  return FileResponse("./web/index.html",headers={"Cache-Control":"no-cache, no-store"})
@app.get("/style.css")
async def style():
  return FileResponse("./web/style.css",headers={"Cache-Control":"no-cache, no-store"})
@app.get("/script.js")
async def script():
  return FileResponse("./web/script.js",headers={"Cache-Control":"no-cache, no-store"})
@app.get("/jQuery.js")
async def jQuery():
  return FileResponse("./web/code.jquery.com_jquery-3.7.1.min.js",headers={"Cache-Control":"no-cache, no-store"})

# 既存のOpenAI API KEYがないか確認
@app.get("/initialization")
async def init():
  if os.getenv('OPENAI_API_KEY') != None:
    return JSONResponse(content={"OpenAI_API_KYE":True},headers={"Cache-Control":"no-cache, no-store"})
  else:
    return JSONResponse(content={"OpenAI_API_KYE":False},headers={"Cache-Control":"no-cache, no-store"})

# 既存のOpenAI API KEYを登録もしくは削除
class APIKEY(BaseModel):
    key: str
@app.post("/API_KEY")
async def SetAPIKey(data:APIKEY):
  if data.key == "":
    if os.getenv('OPENAI_API_KEY') != None:
      os.environ.pop('OPENAI_API_KEY')
    chat_gpt.wakeup_flag = False
    return {"SetAPI":False}
  else:
    os.environ["OPENAI_API_KEY"] = data.key
    chat_gpt.wakeup_flag = False
    return {"SetAPI":True}

# 英会話
class EIKAIWA(BaseModel):
    text: str
@app.post("/EIKAIWA")
async def TalkWithAI(data:EIKAIWA):
  # 一度も起動していない or APIの変更等により再起動が必要な場合 chatgptを再起動
  if not(chat_gpt.wakeup_flag):
    try:
      chat_gpt.wakeup()
    except ValueError:
      print("not set API Key")
      return JSONResponse(content={"error":"API_ERROR"},status_code=500)
  try:
    with get_openai_callback() as cb:
      ans = chat_gpt.conversation.predict(input = data.text)
      print(cb)
      print(cb.total_tokens)
      print(cb.total_cost)
  except error.AuthenticationError:
    print("Ignore API Key")
    os.environ.pop('OPENAI_API_KEY')
    return JSONResponse(content={"error":"API_ERROR"},status_code=500)
  return {"Anser":ans}

# def ConvOpenAI():
#   print(st.session_state.inputconv)

# ブラウザを開く（不要なら削除）
# webbrowser.open("http://127.0.0.1:8000", new=0, autoraise=True)