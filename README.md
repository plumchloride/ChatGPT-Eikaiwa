# ChatGPT-Eikaiwa
ChatGPTを利用した英会話アプリケーション

## 現在制作途中です

![Static Badge](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-green?logo=python&logoColor=white)
![GitHub](https://img.shields.io/github/license/plumchloride/ChatGPT-Eikaiwa?color=blue)

## 使用ライブラリ（主要なもの）
- [OpenAI](https://github.com/openai/openai-python)
- [langchain](https://github.com/langchain-ai/langchain)
- [FastAPI](https://github.com/tiangolo/fastapi)

## 注意事項
- OpenAIのAPIは従量課金制です。会話量や返答が増えると金額も増加します。消し忘れに気をつけて下さい
- APIを利用しています。ブラウザ各社で取得した音声データの取り扱いはブラウザ各社のプライバシーポリシーに準じる形になっているため機密情報等に関しては配慮して下さい

## 導入方法（pyenv + venv）
適当なフォルダにて
```shell
git clone https://github.com/plumchloride/ChatGPT-Eikaiwa.git
cd ./ChatGPT-Eikaiwa
```
### pyenvの設定
```shell
# pyenvに該当のバージョンがない場合
pyenv install 3.11.6

pyenv local 3.11.6
```
### venv作成
```shell
python -m venv .venv
```
### venv起動
```shell
# win
.venv\Scripts\Activate.ps1
# mac
source .venv/bin/activate
```
### pip
```shell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
### 起動
```shell
uvicorn main:app --reload
```