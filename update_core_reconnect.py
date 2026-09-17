import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

# Add flag
if "private var isUserRequestedDisconnect" not in content:
    content = content.replace("private var audioPlayer: AudioPlayer? = null", "private var audioPlayer: AudioPlayer? = null\n    private var isUserRequestedDisconnect = false")

# Update toggleConnection
new_toggle = """    fun toggleConnection() {
        when (_state.value) {
            AssistantState.IDLE, AssistantState.ERROR -> {
                isUserRequestedDisconnect = false
                val apiKey = getApiKey()
                if (apiKey.isEmpty()) {
                    _error.value = "Please enter your Gemini API Key in Settings"
                    return
                }
                
                val persona = getPersona()"""
content = re.sub(r'    fun toggleConnection\(\) \{\s*when \(_state\.value\) \{\s*AssistantState\.IDLE, AssistantState\.ERROR -> \{\s*val apiKey = getApiKey\(\)\s*if \(apiKey\.isEmpty\(\)\) \{\s*_error\.value = "Please enter your Gemini API Key in Settings"\s*return\s*\}\s*val persona = getPersona\(\)', new_toggle, content)

# Update disconnect case
new_disconnect = """            else -> {
                isUserRequestedDisconnect = true
                geminiClient?.disconnect()
            }"""
content = re.sub(r'            else -> \{\s*geminiClient\?\.disconnect\(\)\s*\}', new_disconnect, content)

# Update connectionState listener
old_listener = """        coroutineScope.launch {
            geminiClient?.connectionState?.collect { isConnected ->
                if (isConnected) {
                    _state.value = AssistantState.LISTENING
                    audioRecorder?.startRecording()
                } else {
                    _state.value = AssistantState.IDLE
                    audioRecorder?.stopRecording()
                    audioPlayer?.stopAndClearQueue()
                }
            }
        }"""
new_listener = """        coroutineScope.launch {
            geminiClient?.connectionState?.collect { isConnected ->
                if (isConnected) {
                    _state.value = AssistantState.LISTENING
                    audioRecorder?.startRecording()
                } else {
                    val wasActive = _state.value == AssistantState.LISTENING || _state.value == AssistantState.SPEAKING
                    _state.value = AssistantState.IDLE
                    audioRecorder?.stopRecording()
                    audioPlayer?.stopAndClearQueue()
                    
                    if (wasActive && !isUserRequestedDisconnect) {
                        Log.d("AssistantCore", "Connection dropped, reconnecting...")
                        // small delay to prevent rapid spinning on hard failure
                        kotlinx.coroutines.delay(1000)
                        if (!isUserRequestedDisconnect) {
                            toggleConnection()
                        }
                    }
                }
            }
        }"""
content = content.replace(old_listener, new_listener)

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
