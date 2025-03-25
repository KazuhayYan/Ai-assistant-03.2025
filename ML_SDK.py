from creds import get_iam_token, get_folder_id
import logging
import requests
from Configuration import LOGS, YaGPT_URL, SYSTEM_PROMPT, MAX_GPT_TOKENS

logging.basicConfig(filename=LOGS, level=logging.ERROR, format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

def count_gpt_tokens(messages):
    FOLDER_ID = get_folder_id()
    IAM_TOKEN = get_iam_token()
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion"
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "text": messages
    }
    try:
        return len(requests.post(url=url, json=data, headers=headers).json()['tokens'])
    except Exception as e:
        logging.error(e)
        return 0

def ask_gpt(messages):
    IAM_TOKEN = get_iam_token()
    FOLDER_ID = get_folder_id()
    url = YaGPT_URL
    headers = {
        "Accept": "application/json",
        'Authorization': f'Bearer {IAM_TOKEN}'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": MAX_GPT_TOKENS,
            "reasoningOptions": {
                "mode": "DISABLED"
            }
        },
        "messages": [
            SYSTEM_PROMPT,
            {"role": "user", "text": f"{messages}"}
        ],
        "jsonObject": True
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None
        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        logging.error(e)
        return False, "Ошибка при обращении к GPT", None
