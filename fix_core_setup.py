import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

# Remove audio start from connectionState collect
old_connection_state = """                if (isConnected) {
                    _state.value = AssistantState.LISTENING
                    audioRecorder?.startRecording()
                } else {"""
new_connection_state = """                if (isConnected) {
                    // Do not start recording until setupComplete is received
                    _state.value = AssistantState.CONNECTING
                } else {"""
content = content.replace(old_connection_state, new_connection_state)

# Add setupComplete check in serverMessages collect
old_server_messages = """        coroutineScope.launch {
            geminiClient?.serverMessages?.collect { serverMessage ->
                serverMessage.serverContent?.modelTurn?.parts?.forEach { part ->"""

new_server_messages = """        coroutineScope.launch {
            geminiClient?.serverMessages?.collect { serverMessage ->
                if (serverMessage.setupComplete != null) {
                    Log.d("AssistantCore", "Setup complete received, starting audio recording")
                    _state.value = AssistantState.LISTENING
                    audioRecorder?.startRecording()
                }
                
                serverMessage.serverContent?.modelTurn?.parts?.forEach { part ->"""
content = content.replace(old_server_messages, new_server_messages)

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
