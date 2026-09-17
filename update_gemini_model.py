import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

content = content.replace('"models/gemini-3.1-flash-live-preview"', '"models/gemini-2.0-flash-exp"')

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
