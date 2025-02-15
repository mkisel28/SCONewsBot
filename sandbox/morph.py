import requests
from requests.auth import HTTPBasicAuth
import re
WP_URL = "https://scomedia.ru"
API_ENDPOINT = f"{WP_URL}/wp-json/wp/v2/posts"
USERNAME = "Redaktor"
APP_PASSWORD = "69Ut hkER 9Q4m oCJo iUMR 6Dmk"

raw_content = """*Заголовок*

Текст текст текст _курсив_ *жирный* [ссылка какая то](https://scomedia.ru)
"""


def convert_markdown_to_html(text):
    text = re.sub(r"\*(.*?)\*", r"<strong>\1</strong>", text)  # *жирный*
    text = re.sub(r"_(.*?)_", r"<em>\1</em>", text)  # _курсив_
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', text)  # [ссылка](url)
    return text


formatted_content = convert_markdown_to_html(raw_content)
post_data = {
    "title": "Тестовая новость",
    "content": formatted_content,
    "status": "publish",
    "categories": [],
}

response = requests.post(
    API_ENDPOINT, json=post_data, auth=HTTPBasicAuth(USERNAME, APP_PASSWORD)
)

if response.status_code == 201:
    print("Новость создана в черновиках!")
else:
    print("Ошибка:", response.status_code, response.text)
