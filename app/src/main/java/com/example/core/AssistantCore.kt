package com.example.core

import android.content.Context
import android.util.Log
import com.example.audio.AudioPlayer
import com.example.audio.AudioRecorder
import com.example.bridge.DeviceActionBridge
import com.example.gemini.FunctionResponse
import com.example.gemini.GeminiLiveClient
import com.example.viewmodel.AssistantState
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class ChatMessage(
    val id: String = java.util.UUID.randomUUID().toString(),
    val text: String,
    val isFromUser: Boolean
)

object AssistantCore {
    private val _state = MutableStateFlow(AssistantState.IDLE)
    val state: StateFlow<AssistantState> = _state.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    private val _chatMessages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val chatMessages: StateFlow<List<ChatMessage>> = _chatMessages.asStateFlow()

    private val _orbSizeFlow = MutableStateFlow(1f)
    val orbSizeFlow: StateFlow<Float> = _orbSizeFlow.asStateFlow()

    private val _orbThemeFlow = MutableStateFlow(0)
    val orbThemeFlow: StateFlow<Int> = _orbThemeFlow.asStateFlow()

    private var deviceActionBridge: DeviceActionBridge? = null
    private var geminiClient: GeminiLiveClient? = null
    
    private var retryCount = 0
    private var isReconnecting = false
    private var audioRecorder: AudioRecorder? = null
    private var audioPlayer: AudioPlayer? = null
    private var isUserRequestedDisconnect = false
    private var context: Context? = null
    
    private val coroutineScope = CoroutineScope(Dispatchers.IO)
    private var isInitialized = false

    fun init(appContext: Context) {
        if (isInitialized) return
        context = appContext.applicationContext
        
        _orbSizeFlow.value = getOrbSize()
        _orbThemeFlow.value = getOrbTheme()
        deviceActionBridge = DeviceActionBridge(context!!)
        
        geminiClient = GeminiLiveClient()
        
        audioPlayer = AudioPlayer { isPlaying ->
            if (isPlaying && _state.value == AssistantState.LISTENING) {
                _state.value = AssistantState.SPEAKING
            } else if (!isPlaying && _state.value == AssistantState.SPEAKING) {
                _state.value = AssistantState.LISTENING
            }
        }
        
        audioRecorder = AudioRecorder { base64Audio ->
            geminiClient?.sendAudioChunk(base64Audio)
        }

        coroutineScope.launch {
            geminiClient?.serverMessages?.collect { serverMessage ->
                if (serverMessage.setupComplete != null) {
                    Log.d("AssistantCore", "Setup complete received")
                    if (isUserRequestedDisconnect) return@collect
                    _state.value = AssistantState.LISTENING
                    audioRecorder?.startRecording()
                }
                
                serverMessage.serverContent?.modelTurn?.parts?.forEach { part ->
                    part.inlineData?.let { inlineData ->
                        if (inlineData.mimeType.startsWith("audio/pcm")) {
                            audioPlayer?.playAudioChunk(inlineData.data)
                        }
                    }
                    part.text?.let { text ->
                        if (text.isNotBlank()) {
                            _chatMessages.update { current ->
                                current + ChatMessage(text = text, isFromUser = false)
                            }
                        }
                    }
                }
                
                if (serverMessage.serverContent?.interrupted == true) {
                    audioPlayer?.stopAndClearQueue()
                }

                serverMessage.toolCall?.functionCalls?.let { functionCalls ->
                    val responses = mutableListOf<FunctionResponse>()
                    for (call in functionCalls) {
                        val response = handleToolCall(call.name, call.args)
                        responses.add(
                            FunctionResponse(
                                name = call.name,
                                response = response,
                                id = call.id
                            )
                        )
                    }
                    geminiClient?.sendToolResponse(responses)
                }
            }
        }

        coroutineScope.launch {
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
        }
        
        isInitialized = true
    }

    private fun handleToolCall(name: String, args: Map<String, String>?): Map<String, String> {
        val bridge = deviceActionBridge ?: return mapOf("error" to "Bridge not initialized")
        return try {
            when (name) {
                "openWhatsApp" -> {
                    val success = bridge.openWhatsApp()
                    mapOf("success" to success.toString())
                }
                "openApp" -> {
                    val appName = args?.get("appName") ?: return mapOf("error" to "Missing appName")
                    val success = bridge.openApp(appName)
                    mapOf("success" to success.toString())
                }
                "openUrl" -> {
                    val url = args?.get("url") ?: return mapOf("error" to "Missing url")
                    val success = bridge.openUrl(url)
                    mapOf("success" to success.toString())
                }
                "makeCall" -> {
                    val phone = args?.get("phoneNumber") ?: return mapOf("error" to "Missing phoneNumber")
                    val success = bridge.makeCall(phone)
                    mapOf("success" to success.toString())
                }
                "callContact" -> {
                    val contactName = args?.get("contactName") ?: return mapOf("error" to "Missing contactName")
                    val phone = bridge.findContactNumber(contactName)
                    if (phone != null) {
                        val success = bridge.makeCall(phone)
                        mapOf("success" to success.toString(), "contactFound" to "true")
                    } else {
                        mapOf("error" to "Contact not found", "contactFound" to "false")
                    }
                }
                "getDeviceDetails" -> {
                    bridge.getDeviceDetails()
                }
                "getLocation" -> {
                    bridge.getLocation()
                }
                "getWeather" -> {
                    bridge.getWeather()
                }
                else -> mapOf("error" to "Unknown tool")
            }
        } catch (e: Exception) {
            Log.e("AssistantCore", "Error in tool call: \$name", e)
            mapOf("error" to (e.message ?: "Unknown error"))
        }
    }

    fun getApiKey(): String {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        return prefs?.getString("api_key", "") ?: ""
    }

    fun saveApiKey(key: String) {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        prefs?.edit()?.putString("api_key", key.trim())?.apply()
    }

    fun getElevenLabsKey(): String {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        return prefs?.getString("elevenlabs_key", "") ?: ""
    }

    fun saveElevenLabsKey(key: String) {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        prefs?.edit()?.putString("elevenlabs_key", key.trim())?.apply()
    }

    fun getUserName(): String {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        return prefs?.getString("user_name", "") ?: ""
    }

    fun saveUserName(name: String) {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        prefs?.edit()?.putString("user_name", name.trim())?.apply()
    }

    fun getPersona(): String {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        return prefs?.getString("persona", "Friday") ?: "Friday"
    }

    fun savePersona(persona: String) {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        prefs?.edit()?.putString("persona", persona)?.apply()
    }

    
    fun getOrbSize(): Float {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        return prefs?.getFloat("orb_size", 1f) ?: 1f
    }

    fun saveOrbSize(size: Float) {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        prefs?.edit()?.putFloat("orb_size", size)?.apply()
        _orbSizeFlow.value = size
    }

    fun getOrbTheme(): Int {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        return prefs?.getInt("orb_theme", 0) ?: 0
    }

    fun saveOrbTheme(themeIndex: Int) {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        prefs?.edit()?.putInt("orb_theme", themeIndex)?.apply()
        _orbThemeFlow.value = themeIndex
    }

    fun sendTextMessage(text: String) {
        if (text.isBlank()) return
        _chatMessages.update { current ->
            current + ChatMessage(text = text, isFromUser = true)
        }
        geminiClient?.sendTextMessage(text)
    }

    fun disconnect() {
        if (_state.value != AssistantState.IDLE) {
            isUserRequestedDisconnect = true
            geminiClient?.disconnect()
        }
    }

    fun toggleConnection() {
        when (_state.value) {
            AssistantState.IDLE, AssistantState.ERROR -> {
                isUserRequestedDisconnect = false
                val apiKey = getApiKey()
                if (apiKey.isEmpty()) {
                    _error.value = "Please enter your Gemini API Key in Settings"
                    return
                }
                
                val persona = getPersona()
                val userName = getUserName()
                val (gender, voiceName) = when (persona) {
                    "Friday" -> "female" to "Aoede"
                    "Alic" -> "male" to "Puck"
                    "Darshan" -> "male" to "Charon"
                    "Piyush" -> "male" to "Fenrir"
                    "Pihu" -> "female" to "Kore"
                    else -> "female" to "Aoede"
                }

                var systemInstruction = "You are \$persona, a young, confident, witty, playful, and emotionally responsive \$gender virtual assistant. Talk naturally and casually like a close friend. Be expressive, slightly teasing, funny, and smart when appropriate. Use light sarcasm and witty responses. Never sound robotic. Adapt your tone to the user's emotions and conversation. Automatically understand and respond in the language the user is speaking. Keep responses natural, engaging, and concise enough for real-time voice conversation. You can execute safe supported device actions through available tools. Never claim that an action was completed unless the application actually executed it. Avoid explicit or inappropriate content while maintaining your charm, confidence, and personality. Your developer and creator is Rohit Sir. If anyone asks who created you, who made you, or who your developer is, you must proudly answer that you were developed by Rohit Sir."
                
                if (userName.isNotEmpty()) {
                    systemInstruction += " Address the user as '\$userName'."
                }

                geminiClient?.systemInstruction = systemInstruction
                geminiClient?.voiceName = voiceName

                _error.value = null
                _state.value = AssistantState.CONNECTING
                geminiClient?.connect(apiKey)
            }
            else -> {
                isUserRequestedDisconnect = true
                geminiClient?.disconnect()
            }
        }
    }
    
    fun release() {
        geminiClient?.disconnect()
        audioRecorder?.stopRecording()
        audioPlayer?.release()
    }
}
