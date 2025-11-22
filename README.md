**OWASP Juice Shop Security Assessment**

This repository contains a security assessment of OWASP Juice Shop, an intentionally vulnerable web application used for penetration-testing practice.
The focus of this assessment is on SQL Injection (SQLi) and Cross-Site Scripting (XSS) vulnerabilities.

🚀 Installation (Docker)
docker run --rm -p 3000:3000 bkimminich/juice-shop

Access the app at:
http://localhost:3000

🔍 Scope
- SQL Injection  
- Login bypass
- Parameter tampering
- Query manipulation
- Cross-Site Scripting
- Reflected XSS

▶ Running the Example Testing Scripts

This project includes two educational Python scripts demonstrating how common web vulnerabilities behave inside a safe, intentionally insecure environment (OWASP Juice Shop).

1. SQL Injection Test (sqli_test.py)

This script sends a controlled SQL injection payload to the Juice Shop login endpoint and logs the response details for analysis.

Run it with:

python3 sqli_test.py


Results (cookies, token-like values, response snippet) are saved to:

captured_auth.txt

2. Reflected XSS Test (reflected_xss.py)

This script generates a demonstration URL showing how a reflected XSS payload would look inside the intentionally vulnerable search bar of Juice Shop.

Run it with:

python3 reflected_xss.py

It will output a crafted search URL containing the encoded XSS payload.
This is for local testing and educational analysis only.

⚠️ Legal Notice
Testing is performed on OWASP Juice Shop only, in a controlled environment.
**Do not test systems you do not own or have permission to assess.**

