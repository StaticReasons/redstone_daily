import requests
import json

# 从LLM_keys.json文件中读取API Key和Secret Key
with open("LLM_keys.json", "r") as f:
    data = json.load(f)
    API_KEY = data["API_KEY"]
    SECRET_KEY = data["SECRET_KEY"]


def is_video_compliant(title, description, tags):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_bot_8k?access_token=" + get_access_token()

    prompt = f'''
请根据以下信息判断该视频是否严格符合'我的世界红石科技'的主题，并按照指定的格式回复。

符合要求的包括：红石机器的教程、展示红石机器、描述一个红石机器。
不符合要求的包括：涉及红石的我的世界服务器、在生存模式中建造红石机器、红石音乐等。

请注意：对于信息不足或无法判断的情况，也请按照格式回复'否'。

特别说明: 对于标题中未明确提出有关于'红石科技'内容的(例如'红石','活塞门'等),请直接回复'否'

标题：{title}
简介：{description}
标签：{json.dumps(tags)}

回复格式要求：请直接回复'是'或'否'，无需提供原因或其他文字说明。
'''
    payload = json.dumps({
        "messages": [{"role": "user", "content": prompt}],
        "disable_search": False,
        "enable_citation": False
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"

    # 生成签名
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
