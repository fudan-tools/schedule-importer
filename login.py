import requests
from bs4 import BeautifulSoup;
import subprocess
from urllib.parse import urlparse, parse_qs
import base64
import json;
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
with open("userInfo.json","r") as f:
    file = json.load(f);
    username = file["username"];
    password = file["password"];
session = requests.session();
def jsencrypt_like_encrypt(e: str, t: str) -> str:
    if "BEGIN PUBLIC KEY" in t:
        pem = t
    else:
        s = "".join(t.strip().split())
        pem = "-----BEGIN PUBLIC KEY-----\n" + "\n".join(s[i:i+64] for i in range(0, len(s), 64)) + "\n-----END PUBLIC KEY-----\n"
    pub = serialization.load_pem_public_key(pem.encode("utf-8"))
    data = e.encode("utf-8")
    ct = pub.encrypt(data, padding.PKCS1v15())
    return base64.b64encode(ct).decode("utf-8")
def get_session():
    url = "https://id.fudan.edu.cn/idp/authCenter/authenticate?service=https%3A%2F%2Ffdjwgl.fudan.edu.cn%2Fstudent%2Fsso%2Flogin"
    # 调用 curl，只取响应头
    result = subprocess.run(
        ["curl", "-s", "-D", "-", "-o", "/dev/null", url],
        capture_output=True,
        text=True
    )

    # 解析 Location 字段
    location = None
    for line in result.stdout.splitlines():
        if line.lower().startswith("location:"):
            location = line.split(":", 1)[1].strip()
            break
    parsed = urlparse(location)
    params = parse_qs(parsed.fragment.split("?", 1)[-1])
    lck_value = params.get("lck", [None])[0]
    res = session.get("https://id.fudan.edu.cn/idp/authn/getJsPublicKey");
    key = res.json()["data"];
    encrypted_password = jsencrypt_like_encrypt(password,key)
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://id.fudan.edu.cn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }

    json_data = {
        'authModuleCode': 'userAndPwd',
        'authChainCode': '4cffafe714ad48eeb574714771147063',
        'entityId': 'https://fdjwgl.fudan.edu.cn',
        'requestType': 'chain_type',
        'lck': lck_value,
        'authPara': {
            'loginName': username,
            'password': encrypted_password,
            'verifyCode': '',
        },
    }

    response = session.post('https://id.fudan.edu.cn/idp/authn/authExecute', headers=headers, json=json_data)
    data = response.json();
    token = data["loginToken"];
    res = session.post("https://id.fudan.edu.cn/idp/authCenter/authnEngine?locale=zh-CN",data = {"loginToken":token});
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    ticket = soup.find("input", {"id": "ticket"})["value"]
    params = {
        'ticket': ticket,
        "refer":"https://fdjwgl.fudan.edu.cn/student/for-std/course-table"
    }
    res = session.get("https://fdjwgl.fudan.edu.cn/student/sso/login?",allow_redirects=False,params=params,
                       headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                                });
    return dict(res.cookies)


