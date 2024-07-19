import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI

load_dotenv()

ZHIPU_API_KEY = os.environ["ZHIPU_API_KEY"]

client = ZhipuAI(api_key=ZHIPU_API_KEY)
response = client.chat.completions.create(
    model="glm-4-alltools",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "帮我查询北京今天的天气情况，根据当前的天气，生成一张能提现当前天气状况的图片，精美可爱风格，避免出现违和的内容，突出当前天气下人的状态。"
                }
            ]
        }
    ],
    stream=True,
    tools=[
        {
            "type": "web_browser",
        },
        {
            "type": "drawing_tool"
        }
    ]
)

for chunk in response:
    print(chunk)
