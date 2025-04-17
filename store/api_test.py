import requests

API_KEY = '332a23750c6181cbe4fa87228b4585cfcb2f33ed'
email = 'bituprajapati33@gmail.com'

url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={API_KEY}'

try:
    response = requests.get(url)
    print("Status Code:", response.status_code)
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error: Failed to fetch the data.")
except Exception as e:
    print("An error occurred:", e)
