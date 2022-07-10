import requests

BASE_URL = "http://127.0.0.1:5000/"

data = [
    {"name": "How to Linux", "likes": 1200, "views": 20000},
    {"name": "How to Python", "likes": 1400, "views": 12300},
    {"name": "How to code", "likes": 1500, "views": 143000}
]

def print_response(response):
    print("Status code: {}, response: {}".format(response.status_code, response.json()))

for i in range(len(data)):
    print_response(requests.post(BASE_URL + f"video/{i}", data[i]))

input()

# print_response(requests.delete(BASE_URL + "video/0"))

input()

print_response(requests.get(BASE_URL + "video/20"))
