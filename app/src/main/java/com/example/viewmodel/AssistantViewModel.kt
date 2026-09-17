package com.example.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import com.example.core.AssistantCore

enum class AssistantState {
    IDLE,
    CONNECTING,
    LISTENING,
    SPEAKING,
    ERROR
}

class AssistantViewModel(application: Application) : AndroidViewModel(application) {
    init {
        AssistantCore.init(application)
    }

    val state = AssistantCore.state
    val error = AssistantCore.error
    val chatMessages = AssistantCore.chatMessages

    fun getApiKey(): String = AssistantCore.getApiKey()
    fun saveApiKey(key: String) = AssistantCore.saveApiKey(key)
    
    fun getElevenLabsKey(): String = AssistantCore.getElevenLabsKey()
    fun saveElevenLabsKey(key: String) = AssistantCore.saveElevenLabsKey(key)
    
    fun getUserName(): String = AssistantCore.getUserName()
    fun saveUserName(name: String) = AssistantCore.saveUserName(name)
    
    fun getPersona(): String = AssistantCore.getPersona()
    fun savePersona(persona: String) = AssistantCore.savePersona(persona)
    
    
    fun getWakeWord(): String = AssistantCore.getWakeWord()
    fun saveWakeWord(word: String) = AssistantCore.saveWakeWord(word)

    fun getOrbSize(): Float = AssistantCore.getOrbSize()
    fun saveOrbSize(size: Float) = AssistantCore.saveOrbSize(size)
    
    fun getOrbTheme(): Int = AssistantCore.getOrbTheme()
    fun saveOrbTheme(themeIndex: Int) = AssistantCore.saveOrbTheme(themeIndex)
    
    fun toggleConnection() = AssistantCore.toggleConnection()
    fun sendTextMessage(text: String) = AssistantCore.sendTextMessage(text)

    override fun onCleared() {
        super.onCleared()
        // We do NOT release AssistantCore here, because we want it to live on for the background service
    }
}
