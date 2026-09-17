import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

old_send = """    private fun send(message: ClientMessage) {
        val json = clientMessageAdapter.toJson(message)
        // Log.d("GeminiLiveClient", "Sending message: $json")
        webSocket?.send(json)
    }"""

new_send = """    private fun send(message: ClientMessage) {
        try {
            val json = clientMessageAdapter.toJson(message)
            // Log.d("GeminiLiveClient", "Sending message: $json")
            webSocket?.send(json)
        } catch (e: Exception) {
            Log.e("GeminiLiveClient", "Error serializing/sending message", e)
            _errorMessages.tryEmit("Send error: ${e.message}")
        }
    }"""

content = content.replace(old_send, new_send)

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
