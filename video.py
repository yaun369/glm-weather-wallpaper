import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI
import httpx

load_dotenv()

ZHIPU_API_KEY = os.environ["ZHIPU_API_KEY"]
client = ZhipuAI(api_key=ZHIPU_API_KEY)


def gen_video(title, content, images):
    # 生成视频
    try:
        r = httpx.post(
            "http://localhost:3010/api/making",
            json={
                "title": title,
                "content": content,
                "images": images
            }
        )
        if r.status_code != 200:
            raise Exception(r)
        return r.json()
    except Exception as e:
        print(e)
        return {"error": str(e)}


def alltools_stream():
    response = client.chat.completions.create(
        model="glm-4-alltools",
        messages=[{
            "role": "system",
            "content": "你是一个儿童绘本故事视频生成大师，根据用户输入的绘本主题，生成一个完整的绘本故事。尽可能使用短句，让绘本故事更生动有趣。避免出现暴力、血腥等不合适儿童的内容。根据故事内容使用绘图设计工具生成1张儿童漫画手绘风格图片，最后把故事标题，详细的故事内容，图片地址传给gen_video函数生成视频。"
        }, {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "雷军造车的故事"
                }
            ]
        }],
        stream=True,
        tools=[
            {
                "type": "drawing_tool"
            },
            {
                "type": "function",
                "function": {
                    "name": "gen_video",
                    "description": "根据故事文本和图片地址生成视频",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "description": "大模型生成的故事标题",
                                "type": "string"
                            },
                            "content": {
                                "description": "大模型生成的故事详细内容",
                                "type": "string"
                            },
                            "images": {
                                "description": "图片地址",
                                "type": "string"
                            },
                        },
                        "required": ["title", "content", "images"]
                    }
                }
            },
        ]
    )

    for chunk in response:
        print(chunk)

        choice = chunk.choices[0]
        finish_reason = choice.finish_reason
        tool_calls = choice.delta.tool_calls

        if finish_reason == "tool_calls" and tool_calls and tool_calls[0].type == "function":
            function_call = tool_calls[0].function
            if function_call.name == "gen_video":
                gen_video_args = function_call.arguments.replace(" ", "")
                gen_video_args = eval(gen_video_args)
                print(gen_video_args)
                # gen_video_result = gen_video(**gen_video_args)
                # print(gen_video_result)


if __name__ == "__main__":
    # alltools_stream()
    gen_video_args = {'title': '雷军造车', 
                      'content': '雷军叔叔决定造车了。开始，大家都笑他不懂车。但雷军叔叔不气馁，他带领团队日夜研究，终于造出了一辆特别的电动车。车子不仅好看，而且跑得又快又稳。大家惊喜万分，纷纷试驾。最后，这款车大受欢迎，还赢得了设计大奖。雷军叔叔用他的智慧和勇气，证明了自己能造车。',
                      'images': 'https://sfile.chatglm.cn/testpath/93fbdf9a-eba2-5c80-9c3f-65e9f292b79e_0.png,https://sfile.chatglm.cn/testpath/41b4be44-9c17-5f98-901b-5ce6e389db37_0.png,https://sfile.chatglm.cn/testpath/76fe9d31-afda-5f05-976b-696bfef9e2ff_0.png,https://sfile.chatglm.cn/testpath/7e916155-3e59-5731-af80-0bba0eefaf2f_0.png,https://sfile.chatglm.cn/testpath/41b4be44-9c17-5f98-901b-5ce6e389db37_0.png'}
    gen_video_result = gen_video(**gen_video_args)
