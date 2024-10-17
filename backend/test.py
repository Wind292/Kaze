import requests

def extract_usercombo(url: str):
    return url.split("/")[-2:]

url = 'http://localhost:3000/startnc'
response = requests.get(url)

print(f'Status Code: {response.status_code}')
print(f"{response.json()["message"]}")


url = 'http://localhost:3000/finishnc'  # JavaScript server URL
file_path = r'C:\Rand\JS\Kaze\backend\water.mp4'   # Path to the file you want to send

with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files, data={ "path": extract_usercombo(response.json()["message"]['url']) })

print(response.status_code)  # Should print 200 for success
print(response.text)         # Response from the JS server
