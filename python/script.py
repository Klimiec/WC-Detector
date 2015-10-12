
#  pip install requests


payload = {"id" : "wc1", "state": "ABC"}
url  = "http://localhost:8181/update"
r = requests.put(url, json=payload)
