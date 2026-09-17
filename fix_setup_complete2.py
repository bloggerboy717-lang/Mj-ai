import re

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'r') as f:
    content = f.read()

content = content.replace('class SetupComplete', 'data class SetupComplete(val placeholder: String? = null)')

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'w') as f:
    f.write(content)
