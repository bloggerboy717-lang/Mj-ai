import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

content = content.replace('responseModalities = listOf("AUDIO")', 'responseModalities = listOf("AUDIO", "TEXT")')

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
