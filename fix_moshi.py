import re

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'r') as f:
    content = f.read()

# Replace Map<String, Any>? with SetupComplete?
content = content.replace('val setupComplete: Map<String, Any>? = null', 'val setupComplete: SetupComplete? = null')

# Add SetupComplete data class at the end if it doesn't exist
if 'data class SetupComplete' not in content:
    content += '\n@JsonClass(generateAdapter = true)\ndata class SetupComplete(val dummy: String? = null)\n'

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'w') as f:
    f.write(content)

