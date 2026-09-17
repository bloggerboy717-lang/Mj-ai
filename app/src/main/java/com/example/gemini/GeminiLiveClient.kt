package com.example.gemini

import android.util.Log
import com.example.BuildConfig
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.SharedFlow
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import okio.ByteString
import java.util.concurrent.TimeUnit

class GeminiLiveClient {
    var systemInstruction: String = ""
    var voiceName: String = "Aoede"
    
    private val client = OkHttpClient.Builder()
        .readTimeout(0, TimeUnit.MILLISECONDS)
        .build()

    private var webSocket: WebSocket? = null
    private val moshi = Moshi.Builder().add(KotlinJsonAdapterFactory()).build()
    private val serverMessageAdapter = moshi.adapter(ServerMessage::class.java)
    private val clientMessageAdapter = moshi.adapter(ClientMessage::class.java)

    private val _serverMessages = MutableSharedFlow<ServerMessage>(extraBufferCapacity = 100)
    val serverMessages: SharedFlow<ServerMessage> = _serverMessages

    private val _connectionState = MutableSharedFlow<Boolean>(extraBufferCapacity = 1)
    val connectionState: SharedFlow<Boolean> = _connectionState

    fun connect(apiKey: String) {
        if (apiKey.isEmpty()) {
            Log.e("GeminiLiveClient", "API Key is empty")
            return
        }

        val request = Request.Builder()
            .url("wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key=\$apiKey")
            .build()

        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                Log.d("GeminiLiveClient", "WebSocket Opened")
                _connectionState.tryEmit(true)
                sendSetupMessage()
            }

            override fun onMessage(webSocket: WebSocket, text: String) {
                // Log.d("GeminiLiveClient", "Received text message: \$text")
                try {
                    val message = serverMessageAdapter.fromJson(text)
                    if (message != null) {
                        _serverMessages.tryEmit(message)
                    }
                } catch (e: Exception) {
                    Log.e("GeminiLiveClient", "Error parsing message: \${e.message}")
                }
            }

            override fun onMessage(webSocket: WebSocket, bytes: ByteString) {
                Log.d("GeminiLiveClient", "Received bytes message")
            }

            override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                Log.d("GeminiLiveClient", "WebSocket Closing: \$reason")
                webSocket.close(1000, null)
                _connectionState.tryEmit(false)
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                Log.e("GeminiLiveClient", "WebSocket Error", t)
                _connectionState.tryEmit(false)
            }
        })
    }

    private fun sendSetupMessage() {
        val setupMessage = ClientMessage(
            setup = Setup(
                model = "models/gemini-3.1-flash-live-preview",
                generationConfig = GenerationConfig(
                    responseModalities = listOf("AUDIO"),
                    speechConfig = SpeechConfig(
                        voiceConfig = VoiceConfig(
                            prebuiltVoiceConfig = PrebuiltVoiceConfig(
                                voiceName = voiceName // Dynamic voice (Aoede, Puck, Charon, Kore, Fenrir)
                            )
                        )
                    )
                ),
                systemInstruction = Content(
                    parts = listOf(Part(text = systemInstruction))
                ),
                tools = listOf(
                    Tool(
                        functionDeclarations = listOf(
                            FunctionDeclaration(
                                name = "openWhatsApp",
                                description = "Open WhatsApp application"
                            ),
                            FunctionDeclaration(
                                name = "openApp",
                                description = "Open a specific application by name",
                                parameters = Parameters(
                                    type = "OBJECT",
                                    properties = mapOf("appName" to Property(type = "STRING", description = "The name of the app to open")),
                                    required = listOf("appName")
                                )
                            ),
                            FunctionDeclaration(
                                name = "openUrl",
                                description = "Open a website URL",
                                parameters = Parameters(
                                    type = "OBJECT",
                                    properties = mapOf("url" to Property(type = "STRING", description = "The URL to open")),
                                    required = listOf("url")
                                )
                            ),
                            FunctionDeclaration(
                                name = "makeCall",
                                description = "Initiate a phone call to a given phone number",
                                parameters = Parameters(
                                    type = "OBJECT",
                                    properties = mapOf("phoneNumber" to Property(type = "STRING", description = "The phone number to call")),
                                    required = listOf("phoneNumber")
                                )
                            ),
                            FunctionDeclaration(
                                name = "callContact",
                                description = "Call a contact by their name",
                                parameters = Parameters(
                                    type = "OBJECT",
                                    properties = mapOf("contactName" to Property(type = "STRING", description = "The name of the contact to call")),
                                    required = listOf("contactName")
                                )
                            )
                        )
                    )
                )
            )
        )
        send(setupMessage)
    }

    fun sendTextMessage(text: String) {
        val message = ClientMessage(
            clientContent = ClientContent(
                turns = listOf(
                    Content(
                        role = "user",
                        parts = listOf(Part(text = text))
                    )
                ),
                turnComplete = true
            )
        )
        send(message)
    }

    fun sendAudioChunk(base64PcmData: String) {
        val message = ClientMessage(
            realtimeInput = RealtimeInput(
                mediaChunks = listOf(
                    MediaChunk(
                        mimeType = "audio/pcm;rate=16000",
                        data = base64PcmData
                    )
                )
            )
        )
        send(message)
    }

    fun sendToolResponse(functionResponses: List<FunctionResponse>) {
        val message = ClientMessage(
            toolResponse = ToolResponseMessage(
                functionResponses = functionResponses
            )
        )
        send(message)
    }

    private fun send(message: ClientMessage) {
        try {
            val json = clientMessageAdapter.toJson(message)
            webSocket?.send(json)
        } catch (e: Exception) {
            Log.e("GeminiLiveClient", "Error sending message", e)
        }
    }

    fun disconnect() {
        webSocket?.close(1000, "User disconnected")
        webSocket = null
        _connectionState.tryEmit(false)
    }
}
