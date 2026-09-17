import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

content = content.replace('"object"', '"OBJECT"').replace('"string"', '"STRING"')

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
