import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

content = content.replace('    private var isUserRequestedDisconnect = false\n                hasFatalError = false\n    private var context: Context? = null', '    private var isUserRequestedDisconnect = false\n    private var context: Context? = null')

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
