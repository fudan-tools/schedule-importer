import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from public import login;
import requests
def get_session():
    ticket = login.get_ticket("https://fdjwgl.fudan.edu.cn/student/sso/login");
    params = {
        'ticket': ticket,
    }
    res = requests.get("https://fdjwgl.fudan.edu.cn/student/sso/login?",allow_redirects=False,params=params,
                           headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                                    });
    return dict(res.cookies)