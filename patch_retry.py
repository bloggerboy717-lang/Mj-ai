import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

# Add retry variables
new_vars = """    private var deviceActionBridge: DeviceActionBridge? = null
    private var geminiClient: GeminiLiveClient? = null
    
    private var retryCount = 0
    private var isReconnecting = false"""

content = content.replace('    private var deviceActionBridge: DeviceActionBridge? = null\n    private var geminiClient: GeminiLiveClient? = null', new_vars)

old_collect = """        coroutineScope.launch {
            geminiClient?.connectionState?.collect { isConnected ->
                if (isConnected) {
                    // Do not start recording until setupComplete is received
                    _state.value = AssistantState.CONNECTING
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

new_collect = """        coroutineScope.launch {
            geminiClient?.connectionState?.collect { isConnected ->
                if (isConnected) {
                    // Reset retry variables on successful connection
                    retryCount = 0
                    isReconnecting = false
                    // Do not start recording until setupComplete is received
                    _state.value = AssistantState.CONNECTING
                } else {
                    val wasActive = _state.value == AssistantState.LISTENING || _state.value == AssistantState.SPEAKING || _state.value == AssistantState.CONNECTING
                    _state.value = AssistantState.IDLE
                    audioRecorder?.stopRecording()
                    audioPlayer?.stopAndClearQueue()
                    
                    if ((wasActive || isReconnecting) && !isUserRequestedDisconnect && retryCount < 5) {
                        isReconnecting = true
                        val delayTime = (1000.0 * Math.pow(2.0, retryCount.toDouble())).toLong()
                        Log.d("AssistantCore", "Connection dropped, reconnecting in ${delayTime}ms (Attempt ${retryCount + 1})")
                        
                        _error.value = "Connection dropped. Reconnecting... (${retryCount + 1}/5)"
                        
                        kotlinx.coroutines.delay(delayTime)
                        
                        if (!isUserRequestedDisconnect) {
                            retryCount++
                            toggleConnection()
                        }
                    } else if (retryCount >= 5) {
                        _error.value = "Failed to reconnect. Please try again."
                        isReconnecting = false
                        retryCount = 0
                    }
                }
            }
        }"""

if old_collect in content:
    content = content.replace(old_collect, new_collect)
    print("Replaced collection block")
else:
    print("WARNING: Could not find old_collect block")
    
with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)

