import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

# Make sure we don't throw if websocket is null
new_send = """    private fun send(message: ClientMessage) {
        try {
            if (webSocket == null) return
            val json = clientMessageAdapter.toJson(message)
            webSocket?.send(json)
        } catch (e: Exception) {
            Log.e("GeminiLiveClient", "Error sending message", e)
        }
    }"""
content = re.sub(r'    private fun send\(message: ClientMessage\) \{[\s\S]*?\}', new_send, content)

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
