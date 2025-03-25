import json
from Configuration import HOME_DIR

def get_folder_id():
    with open(f'{HOME_DIR}/creds/folder_id.txt', 'r') as s:
        FOLDER_ID = s.read().strip()
        return FOLDER_ID

def get_iam_token():
    with open(f'{HOME_DIR}/creds/iam_token.txt', 'r') as s:
        file_data = json.load(s)
        IAM_TOKEN = file_data["access_token"]
        return IAM_TOKEN

def get_bot_token():
    with open(f'{HOME_DIR}/creds/bot_token.txt', 'r') as s:
        BOT_TOKEN = s.read().strip()
        return BOT_TOKEN