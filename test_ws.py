import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

# Make sure it only sends AUDIO to avoid setup failure
content = content.replace('responseModalities = listOf("AUDIO", "TEXT")', 'responseModalities = listOf("AUDIO")')

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
