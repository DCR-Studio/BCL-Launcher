import os
import secrets
import asyncio
import fastapi
import webbrowser
import json
import requests
from types import SimpleNamespace
from fastapi import FastAPI, Request
import uvicorn
from urllib.parse import urlencode, urljoin

app = FastAPI()
callback_event = asyncio.Event()

msat = None
reppwd = None
state = None

def prelogin():
  """返回所有配置值，封装为一个对象"""
  return SimpleNamespace(
      clientid="87acf5d5-124c-4dfc-a9db-6ef7cfa4b955",
      client_secret="7iD8Q~rM9MEe2wdc6AKHUllcmCS69D5QOvA8cczD",
      redirect_url="http://localhost:42747/msauth",
      baseurl="https://login.microsoftonline.com",
      xboxserurl="https://user.auth.xboxlive.com/user/authenticate",
      xstsserver="https://xsts.auth.xboxlive.com/xsts/authorize",
      mcapiurl="https://api.minecraftservices.com/authentication/login_with_xbox",
      auth_pth="/consumers/oauth2/v2.0/authorize?",
      actk_pth="/consumers/oauth2/v2.0/token",
      scope="XboxLive.signin offline_access",
      state=secrets.token_urlsafe(32)
  )#登录开始前定义登录所需的参数

def mklink(baseurl, path="", **args):
  query_string = urlencode(args)
  return urljoin(baseurl, f"{path}?{query_string}")#拼接链接

def repmsautk(config):
  global msauthtk, reppwd
  logurl = mklink(config.baseurl, config.auth_pth, 
            client_id=config.clientid, 
            response_type="code", 
            redirect_uri=config.redirect_url, 
            scope=config.scope, 
            state=config.state)
  msauthtk = config.state
  print("Please complete the operation within the opened browser window. If it is not opened, please copy the following link to open it in your browser:")
  print(logurl)
  webbrowser.open(logurl)#获取微软账户访问密钥

def repmsactk(config):
  global msactk
  geturl = mklink(config.baseurl, config.actk_pth, 
            client_id=config.clientid, 
            code=reppwd, 
            redirect_uri=config.redirect_url, 
            grant_type="authorization_code", 
            client_secret=config.client_secret)
  headers = {"Content-Type": "application/x-www-form-urlencoded"}
  data = {
      "client_id": config.clientid,
      "scope": config.scope,
      "code": reppwd,
      "redirect_uri": config.redirect_url,
      "grant_type": "authorization_code",
      "client_secret": config.client_secret
  }
    
  response = requests.post(geturl, headers=headers, data=urlencode(data))
  if response.status_code == 200:
      token_data = response.json()
      msactk = token_data.get("access_token")
      print(f"Access token received, Getting XBL......")
  else:
      print(f"Error retrieving token: {response.status_code}, {response.text}")#获取微软账户通行令牌

def repxbl(config, msactk):
  headers = {
      "Content-Type": "application/json",
      "Accept": "application/json"
  }
  data = {
      "Properties": {
          "AuthMethod": "RPS",
          "SiteName": "user.auth.xboxlive.com",
          "RpsTicket": f"d={msactk}"  # 使用 msactk 获取 token
      },
      "RelyingParty": "http://auth.xboxlive.com",
      "TokenType": "JWT"
  }
    
  response = requests.post(config.xboxserurl, headers=headers, json=data)
    
  if response.status_code == 200:
      # 如果请求成功，处理返回的数据
      token_data = response.json()  # 将响应的JSON数据转换为字典
      xboxlivekey = token_data.get("Token")  # 获取 accesstoken
      print(f"XBL received, Getting XSTS......")
      return xboxlivekey
  else:
      print(f"Error retrieving XBL: {response.status_code}, {response.text}")#获取XBL令牌

def repxsts(config, xboxlivekey):
  global xblkey
  xblkey = xboxlivekey
  headers = {
      "Content-Type": "application/json",
      "Accept": "application/json"
  }
  data = {
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [xblkey]  # 注意此处要使用变量 xblkey
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
  }
    
  response = requests.post(config.xstsserver, headers=headers, json=data)
  response.raise_for_status()
  response_data = response.json()
    
  if response.status_code == 200:
      # 如果请求成功，处理返回的数据
      token_data = response.json()  # 将响应的JSON数据转换为字典
      xstskey = token_data.get("Token")  # 获取 access token
      print(f"XSTS received, Getting UserInfo......")
      uhs = response_data["DisplayClaims"]["xui"][0]["uhs"]
  else:
      print(f"Error retrieving XBL: {response.status_code}, {response.text}")#获取XSTS令牌

def repmcusin(config, xstskey):
  global uhs
  print(uhs)
  headers = {
      "Content-Type": "application/json",
      "Accept": "application/json"
  }
  data = {
    "identityToken": "XBL3.0 x=uhs;xstsk"
  }
  print(config.mcapiurl, headers, data)
  response = requests.post(config.mcapiurl, headers=headers, json=data)
  
    
  if response.status_code == 200:
      # 如果请求成功，处理返回的数据
      token_data = response.json()  # 将响应的JSON数据转换为字典
      mcat = token_data.get("access_token")  # 获取 access token
      print(f"MCAT received, Getting UserInfo......")
  else:
      print(f"Error retrieving MCAT: {response.status_code}, {response.text}")#获取Minecraft账户访问令牌

def verifyms(received_state):#获取访问密钥时验证服务器
  global msauthtk
  if msauthtk == received_state:
      print("State matches, request is valid.")
      callback_event.set()
      return True
  else:
      print("Login request tampered!")
      return False

@app.get("/msauth")
async def handle_callback(request: Request, code: str, state: str):
  global msat, reppwd
  reppwd = code
  print(f"Code received")
  print(f"State received")
  mser = verifyms(state)
  return {"status": "success" if mser else "error", "code": code, "state": state}

@app.get("/favicon.ico")
async def favicon():
  return fastapi.responses.RedirectResponse(url='/static/favicon.ico')

async def loginapiserver():
  config = uvicorn.Config(app, host="0.0.0.0", port=42747)
  las = uvicorn.Server(config)
  await las.serve()

async def main():
  config = prelogin()
  print("Start login server daemon")
  asyncio.create_task(loginapiserver())
  print("Daemon Listen Started")
  print("Generating Login Link......")
  repmsautk(config)
  await callback_event.wait()
  print("Getting Microsoft Account AccessToken......")
  repmsactk(config)
  print("Getting Xbox Live key......")
  xboxlivekey = repxbl(config, msactk)
  print("Getting XSTS......")
  xstskey = repxsts(config, xboxlivekey)
  print("Getting MCAT")
  mcat = repmcusin(config, xstskey)

if __name__ == "__main__":
  asyncio.run(main())