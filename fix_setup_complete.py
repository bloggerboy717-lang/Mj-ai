import re

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'r') as f:
    content = f.read()

content = content.replace('val setupComplete: Map<String, String>? = null', 'val setupComplete: SetupComplete? = null')

new_class = """
@JsonClass(generateAdapter = true)
class SetupComplete
"""

content = content + new_class

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'w') as f:
    f.write(content)
