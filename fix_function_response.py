import re

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'r') as f:
    content = f.read()
content = content.replace('val response: Map<String, String>,', 'val response: Map<String, Any>,')
with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()
content = content.replace('private fun handleToolCall(name: String, args: Map<String, String>?): Map<String, String>', 'private fun handleToolCall(name: String, args: Map<String, String>?): Map<String, Any>')
with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
