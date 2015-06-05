import requests

login_url = "https://www.douban.com/accounts/login"

do_login_url = "https://accounts.douban.com/login"

session = requests.session()

session.get(login_url)

payload = {
    "form_email":"",
    "form_password":""
}

response = session.post(do_login_url, payload)

print response.text.encode("utf-8")



