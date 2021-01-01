import requests

url = "https://discord.com/api/v8/applications/<app id>/guilds/<guild id>/commands"

json = {
    "name": "히요비정보",
    "description": "히요비에서 해당작품 정보를 가져옵니다.",
    "options": [
        {
            "name": "번호",
            "description": "작품번호",
            "type": 3,
            "required": True,
        }
    ],
}
headers = {"Authorization": "Bot Token"}


res = requests.post(url, headers=headers, json=json)

print(res.text, res.status_code)
