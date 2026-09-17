import re

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'r') as f:
    content = f.read()

content = content.replace('@JsonClass(generateAdapter = true)\nclass SetupComplete\n', '')

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'w') as f:
    f.write(content)
