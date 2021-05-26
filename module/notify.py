import requests


def notify():
    PUSH_KEY = 'SCT27848T2MtRBqnA5m3mQm8TuJa6Y2ko'
    _d = {
        "desp": '1'
    }
    _d["text"] = "coverage-tool  挂了呀~阳哥赶紧的呀~"

    resp = requests.post(f"https://sctapi.ftqq.com/{PUSH_KEY}.send", data=_d)
    print(resp.text)