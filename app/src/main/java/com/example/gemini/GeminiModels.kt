package com.example.gemini

import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class ClientMessage(
    val setup: Setup? = null,
    val realtimeInput: RealtimeInput? = null,
    val clientContent: ClientContent? = null,
    val toolResponse: ToolResponseMessage? = null
)

@JsonClass(generateAdapter = true)
data class Setup(
    val model: String,
    val generationConfig: GenerationConfig? = null,
    val systemInstruction: Content? = null,
    val tools: List<Tool>? = null
)

@JsonClass(generateAdapter = true)
data class GenerationConfig(
    val responseModalities: List<String>? = null,
    val speechConfig: SpeechConfig? = null
)

@JsonClass(generateAdapter = true)
data class SpeechConfig(
    val voiceConfig: VoiceConfig
)

@JsonClass(generateAdapter = true)
data class VoiceConfig(
    val prebuiltVoiceConfig: PrebuiltVoiceConfig
)

@JsonClass(generateAdapter = true)
data class PrebuiltVoiceConfig(
    val voiceName: String
)

@JsonClass(generateAdapter = true)
data class Content(
    val role: String? = null,
    val parts: List<Part>
)

@JsonClass(generateAdapter = true)
data class Part(
    val text: String? = null,
    val inlineData: InlineData? = null
)

@JsonClass(generateAdapter = true)
data class InlineData(
    val mimeType: String,
    val data: String
)

@JsonClass(generateAdapter = true)
data class Tool(
    val functionDeclarations: List<FunctionDeclaration>
)

@JsonClass(generateAdapter = true)
data class FunctionDeclaration(
    val name: String,
    val description: String,
    val parameters: Parameters? = null
)

@JsonClass(generateAdapter = true)
data class Parameters(
    val type: String,
    val properties: Map<String, Property>? = null,
    val required: List<String>? = null
)

@JsonClass(generateAdapter = true)
data class Property(
    val type: String,
    val description: String? = null
)

@JsonClass(generateAdapter = true)
data class RealtimeInput(
    val mediaChunks: List<MediaChunk>
)

@JsonClass(generateAdapter = true)
data class MediaChunk(
    val mimeType: String,
    val data: String
)

@JsonClass(generateAdapter = true)
data class ClientContent(
    val turns: List<Content>,
    val turnComplete: Boolean? = null
)

@JsonClass(generateAdapter = true)
data class ToolResponseMessage(
    val functionResponses: List<FunctionResponse>
)

@JsonClass(generateAdapter = true)
data class FunctionResponse(
    val name: String,
    val response: Map<String, String>,
    val id: String
)

// Server responses

@JsonClass(generateAdapter = true)
data class ServerMessage(
    val setupComplete: SetupComplete? = null,
    val serverContent: ServerContent? = null,
    val toolCall: ToolCallMessage? = null
)

@JsonClass(generateAdapter = true)
data class ServerContent(
    val modelTurn: Content? = null,
    val turnComplete: Boolean? = null,
    val interrupted: Boolean? = null
)

@JsonClass(generateAdapter = true)
data class ToolCallMessage(
    val functionCalls: List<FunctionCall>
)

@JsonClass(generateAdapter = true)
data class FunctionCall(
    val name: String,
    val args: Map<String, String>? = null,
    val id: String
)

@JsonClass(generateAdapter = true)
data class SetupComplete(val placeholder: String? = null)
