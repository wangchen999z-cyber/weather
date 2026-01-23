from urllib import request, parse
import requests 

import pandas as pd
import json

url_b="https://api.seniverse.com/v3/weather/daily.json?key=SQPq5cHK4nKMN6fvb&location=beijing&language=zh-Hans&unit=c&start=0&days=7"
url_t="https://api.seniverse.com/v3/weather/daily.json?key=SQPq5cHK4nKMN6fvb&location=tianjin&language=zh-Hans&unit=c&start=0&days=7"
# 构建请求
req_b = request.Request(url_b)
# 发送请求，读取返回值并进行 UTF-8 编码
response_b = request.urlopen(req_b).read().decode('UTF-8')
response_b = json.loads(response_b)


req_t = request.Request(url_t)
# 发送请求，读取返回值并进行 UTF-8 编码
response_t = request.urlopen(req_t).read().decode('UTF-8')
response_t = json.loads(response_t)


# 提取 daily 数据
df_b = pd.DataFrame(response_b["results"][0]["daily"])

# 选择需要的列，并修改列名
df_b = df_b[["date", "text_day", "high", "low", "rainfall", "humidity", "wind_scale"]]
df_b.columns = ["日期", "天气", "最高温(°C)", "最低温(°C)", "降水量(mm)", "湿度(%)", "风力"]


# 提取 daily 数据
df_t = pd.DataFrame(response_t["results"][0]["daily"])

# 选择需要的列，并修改列名
df_t = df_t[["date", "text_day", "high", "low", "rainfall", "humidity", "wind_scale"]]
df_t.columns = ["日期", "天气", "最高温(°C)", "最低温(°C)", "降水量(mm)", "湿度(%)", "风力"]


# 设置索引为日期
df_b.set_index("日期", inplace=True)

url2 = "https://open.feishu.cn/open-apis/bot/v2/hook/a095e47f-59f5-493b-a6d8-6394f1b5409b"



daily_forecast_b = response_b["results"][0]["daily"]
daily_forecast_t = response_t["results"][0]["daily"]

message_b = "北京未来三天天气预报：\n"
for day in daily_forecast_b:
    message_b += f"{day['date']}: {day['text_day']}，气温{day['low']}~{day['high']}°C，降水量{day['rainfall']}mm，湿度{day['humidity']}%，风力{day['wind_scale']}级\n"


message_t = "天津未来三天天气预报：\n"
for day in daily_forecast_t:
    message_t += f"{day['date']}: {day['text_day']}，气温{day['low']}~{day['high']}°C，降水量{day['rainfall']}mm，湿度{day['humidity']}%，风力{day['wind_scale']}级\n"

# 构造 POST 请求的 payload
payload_b = {
    "msg_type": "text",  # 适用于飞书、钉钉等
    "content": {"text": message_b}
}

# 构造 POST 请求的 payload
payload_t = {
    "msg_type": "text",  # 适用于飞书、钉钉等
    "content": {"text": message_t}
}



# 发送 POST 请求
headers = {"Content-Type": "application/json"}
response_b = requests.post(url2, data=json.dumps(payload_b), headers=headers)
response_t = requests.post(url2, data=json.dumps(payload_t), headers=headers)

# 打印响应
print(response_b.status_code, response_b.text,response_t.status_code, response_t.text)



