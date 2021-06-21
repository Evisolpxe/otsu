### 如何运行

运行环境: *Python3.8+*, *Mongodb*

```
# 安装虚拟环境
pip install pipenv
# 创建环境
pipenv install
cd otsu && cp .env.sample .env

# 填入mongo的连接串(本地环境可不填，自动连接)和你的osu api
vim .env

# 运行
uvicorn run:app --reload
```
