import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

content = content.replace('    fun toggleConnection() {', '    fun disconnect() {\n        if (_state.value != AssistantState.IDLE) {\n            isUserRequestedDisconnect = true\n            geminiClient?.disconnect()\n        }\n    }\n\n    fun toggleConnection() {')

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
