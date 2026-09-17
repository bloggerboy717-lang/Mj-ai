import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

old_failure = """            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                Log.e("GeminiLiveClient", "WebSocket Error", t)
                _connectionState.tryEmit(false)
            }"""

new_failure = """            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                val errorMsg = "WebSocket Error: ${t.message}" + if (response != null) " (HTTP ${response.code})" else ""
                Log.e("GeminiLiveClient", errorMsg, t)
                _errorMessages.tryEmit(errorMsg)
                _connectionState.tryEmit(false)
            }"""

content = content.replace(old_failure, new_failure)

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
