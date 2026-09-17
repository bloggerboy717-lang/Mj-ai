import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

old_closing = """            override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                Log.d("GeminiLiveClient", "WebSocket Closing: $reason")
                webSocket.close(1000, null)
                _connectionState.tryEmit(false)
            }"""

new_closing = """            override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                Log.d("GeminiLiveClient", "WebSocket Closing: $code - $reason")
                if (code != 1000) {
                    _errorMessages.tryEmit("Server closed connection ($code): $reason")
                }
                webSocket.close(1000, null)
                _connectionState.tryEmit(false)
            }"""

content = content.replace(old_closing, new_closing)

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
