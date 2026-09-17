import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

# Add a flow for parsing errors
content = content.replace(
    'val connectionState: SharedFlow<Boolean> = _connectionState',
    'val connectionState: SharedFlow<Boolean> = _connectionState\n\n    private val _errorMessages = MutableSharedFlow<String>(extraBufferCapacity = 1)\n    val errorMessages: SharedFlow<String> = _errorMessages'
)

# Emit parsing error
content = content.replace(
    'Log.e("GeminiLiveClient", "Error parsing message: ${e.message}")',
    'Log.e("GeminiLiveClient", "Error parsing message: ${e.message}")\n                    _errorMessages.tryEmit("Parsing error: ${e.message}")'
)

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)


with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

# Collect error messages
collect_error = """        coroutineScope.launch {
            geminiClient?.errorMessages?.collect { err ->
                _error.value = "Gemini Error: $err"
                // Maybe disconnect if fatal, but let's just show it
            }
        }
        
        coroutineScope.launch {"""

content = content.replace('        coroutineScope.launch {\n            geminiClient?.connectionState?.collect', collect_error + '\n            geminiClient?.connectionState?.collect')

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
