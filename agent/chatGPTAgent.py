import os
import openai
from diskcache import Cache

openai.api_key = ""

# 实例一个缓存对象，缓存对话记录，让gpt对话具有上下文
# 需要传入目录路径。如果目录路径不存在，将创建该路径，并且会在指定位置创建一个cache.db的文件。
# 如果未指定，则会自动创建一个临时目录，并且会在指定位置创建一个cache.db的文件。
cache = Cache('./cache01')


def ask(text):
    chat_record = cache.get('chat_record', default=False, retry=True)
    if not chat_record:
        first_value = "Human: " + text + "\nAI: "
        cache.set('chat_record', first_value, expire=600, read=True, retry=True)
        prompt = "Human: " + text + "\nAI: "
    else:
        prompt = chat_record + "Human: " + text + "\nAI: "
    # print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    # print(response)
    result = response.get("choices")[0].get("text")
    value = prompt + result + "\n"
    cache.set('chat_record', value, expire=600, read=True, retry=True)
    return result


