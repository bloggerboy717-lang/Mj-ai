import json

data = """{
  "setupComplete": {}
}"""

print(json.dumps(json.loads(data)))
