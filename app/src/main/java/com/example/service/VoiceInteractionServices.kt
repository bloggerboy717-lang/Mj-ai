package com.example.service

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.service.voice.VoiceInteractionService
import android.service.voice.VoiceInteractionSession
import android.service.voice.VoiceInteractionSessionService

class MyVoiceInteractionService : VoiceInteractionService()

class MyVoiceInteractionSessionService : VoiceInteractionSessionService() {
    override fun onNewSession(args: Bundle?): VoiceInteractionSession {
        return MyVoiceInteractionSession(this)
    }
}

class MyVoiceInteractionSession(context: Context) : VoiceInteractionSession(context) {
        override fun onShow(args: Bundle?, showFlags: Int) {
        super.onShow(args, showFlags)
        val intent = Intent(context, com.example.MainActivity::class.java).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
        }
        context.startActivity(intent)
        
        // Start assistant automatically
        if (com.example.core.AssistantCore.state.value == com.example.viewmodel.AssistantState.IDLE) {
            com.example.core.AssistantCore.toggleConnection()
        }
    }
}
