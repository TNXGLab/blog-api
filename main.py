# 引入fastapi
from fastapi import FastAPI, Request
import uvicorn
import os

from tools.xdbSearcher import XdbSearcher

# 实例化一个FastAPI对象
app = FastAPI()

# 设置全局的cors返回头


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Expose-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["source"] = "Preliminary Rodesisland Terminal System(PRTS)"
    return response

# 定义路由


@app.get("/")
async def root():
    return {"code": "200", "message": "这里是天翔TNXGの空间站的api接口！使用基于Python的Fastapi搭建，部分信息会从这里汇总发布！"}


@app.get("/ping")
async def ping():
    return {"code": "200", "message": "pong"}


@app.get("/ip2region")
async def ip2region(request: Request, ip: str = None):
    if ip is None:
        return request.headers['X-Real-IP']
    try:
        dbPath = os.path.join(os.path.dirname(
            __file__), "./data/ip2region.xdb")
        searcher = XdbSearcher(dbfile=dbPath)
        region_str = searcher.searchByIPStr(ip).replace('|0', '')
        searcher.close()
        region_list = region_str.split('|')
        location_str = ''
        for i in region_list:
            location_str = location_str + i + ' '
        location_str = location_str.strip()
        return {"code": "200", "message": "success", "ip": ip, "location": location_str}
    except:
        return {"code": "500", "message": "error"}


# 获取系统环境变量LEANCLOUD_APP_PORT
port = os.getenv('LEANCLOUD_APP_PORT')
