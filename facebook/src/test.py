import requests

if __name__ == "__main__":

    response = requests.get("http://m.facebook.com")

    print response.text
