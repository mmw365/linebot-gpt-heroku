## このアプリケーションについて

OpenAIのAPIを使ったチャットボットです。Heroku上で動きます。

## 使い方

- LINEのチャネルを作成し、チャネルアクセストークンを発行する
- OpenAIのAPI Keyを取得する
- Herokuにデプロイする
- LINEチャネルのWebhook設定にURLを指定し、Webhookの利用をオンにする

## Herokuへのデプロイ方法

- 以下のコマンドを実行する
```
heroku login

git clone https://github.com/mmw365/linebot-gpt-heroku.git linebot-gpt-heroku
cd linebot-gpt-heroku
heroku apps:create linebot-gpt-heroku
git push heroku main

heroku config:set LINE_ACCESS_TOKEN=<LINE Channel Access Token>
heroku config:set OPENAI_API_KEY=<OpenAI API Key>
```
## ローカル環境（VENVの設定）
```
python.exe -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## ローカル環境での実行方法
```
uvicorn main:app --reload
```
もしくは
```
heroku local --port 5001
```
