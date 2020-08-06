Git Auto Pull
===


Index
---
- [Git Auto Pull](#git-auto-pull)
  - [Index](#index)
  - [Guide](#guide)
  - [設定環境](#設定環境)
    - [條件](#條件)
  - [步驟](#步驟)
    - [新增flask app](#新增flask-app)
    - [Fork gitlab repo](#fork-gitlab-repo)
    - [Start flask app](#start-flask-app)
    - [Test](#test)

Guide
---
  1. 在gitlab 或是 github中 ，設定repository 的 webhook
  2. 到你想要自動更新專案的server上，新增一個main.py並啟動
  3. 當發生push event時，server會接到webhook並自動pull repository
  4. 自動部屬程式到生產環境就完成了


設定環境
---
```
測試用環境 : Raspberry PI 3
```
### 條件
- 要部屬的Server必須先在```gitlab``` 或是 ```github``` 上新增ssh key，且本地端也要有ssh key。
- 需先安裝好python3(建議使用python3.6以上)，且有flask 套件
```
pip install flask
```


步驟
---

### 新增flask app
- 在server的資料夾內新增一個 ```main.py```
  ```python
  #main.py
  from flask import jsonify,request,Flask
  import subprocess
  from pathlib import Path,PurePath
  app = Flask(__name__)

  @app.route('/')
  def api_root():
      return "welcome to github auto deploy"

  @app.route('/webhook',methods=['POST'])
  def webhook():
      data = request.json
      repository_name = data['repository']['name']
      p = subprocess.run("cd %s && git pull"%repository_name, shell=True,cwd=Path(__file__).parent.absolute())
      return ""

  if __name__ == '__main__':
      app.run('0.0.0.0',debug=True)
  ```

### Fork gitlab repo
這邊需要一個repo來驗證flask + webhook，如果有自己的repo的話可以用自己的，沒有的話可以參考下方的說明


因此這邊先使用GitLab-examples上的[redis](https://gitlab.com/gitlab-examples/redis)這個repo

1. 把這個repo fork到自己的git裡面
2. 再把這個repo clone到 server 的 main.py 旁邊(下圖為示意圖)
> 這時clone repo應該是不需要打密碼的，因為有做了新增ssh key了

```
project
│───main.py  
│
└───redis
│   │───file011.txt
│   │
└───other repo1
│   │───test.txt
│   │
└───other repo2
│   │───test.txt

```


3. 到```設定```的```webhook```分頁，在URL的輸入框下填上剛剛設定好的flask route 
   
  ```
  #URL
  http://<你的IP>:5000/webhook
  
  #範例
  http://100.100.100.100:5000/webhook
  ```
接著選擇 ```Add webhook```

### Start flask app
啟動flask app
```
python3 main.py
```

接著會看到```新增webhook```的頁面，最下面有剛剛新增好的webhook紀錄

旁邊有個```test```，選擇```push event```

就會看到console上出現了status code為200，且出現
```
Already up to date.
```
代表webhook已經設定完成了

### Test
當觸發push event時，是否真的會自動更新?

這邊可以去修改 redis repo 下的 ```README.md```
- 用網頁點一下```README.md```，選擇```編輯```
- 隨便輸入幾行字後commit

接著就會看到flask又接到新的push event

看看```README.md```，會發現剛剛新增的文字在上面了

--完--
