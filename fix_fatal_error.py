import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

# Add hasFatalError
content = content.replace(
    'private var isReconnecting = false',
    'private var isReconnecting = false\n    private var hasFatalError = false'
)

# Reset hasFatalError on connect
content = content.replace(
    'isUserRequestedDisconnect = false',
    'isUserRequestedDisconnect = false\n                hasFatalError = false'
)

# Set hasFatalError on errorMessages
error_collect = """        coroutineScope.launch {
            geminiClient?.errorMessages?.collect { err ->
                _error.value = "Gemini Error: $err"
                hasFatalError = true
            }
        }"""
content = re.sub(r'        coroutineScope\.launch \{\s*geminiClient\?\.errorMessages\?\.collect \{ err ->\s*_error\.value = "Gemini Error: \$err"\s*// Maybe disconnect if fatal, but let\'s just show it\s*\}\s*\}', error_collect, content)

# Prevent reconnect if fatal
old_reconnect = 'if ((wasActive || isReconnecting) && !isUserRequestedDisconnect && retryCount < 5) {'
new_reconnect = 'if ((wasActive || isReconnecting) && !isUserRequestedDisconnect && !hasFatalError && retryCount < 5) {'
content = content.replace(old_reconnect, new_reconnect)

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)

