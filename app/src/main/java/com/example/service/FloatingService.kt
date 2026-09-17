package com.example.service

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.graphics.PixelFormat
import android.os.Build
import android.os.IBinder
import android.view.Gravity
import android.view.WindowManager
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.ComposeView
import androidx.compose.ui.unit.dp
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.foundation.background
import androidx.compose.foundation.shape.CircleShape
import androidx.core.app.NotificationCompat
import androidx.lifecycle.*
import androidx.savedstate.*

import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.os.Bundle
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import android.Manifest
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat
import com.example.core.AssistantCore
import com.example.ui.theme.MyApplicationTheme
import com.example.viewmodel.AssistantState

class FloatingService : Service() {
    private lateinit var windowManager: WindowManager
    private lateinit var composeView: ComposeView
    private val lifecycleOwner = FloatingLifecycleOwner()
    
    private var paramsX = 100
    private var paramsY = 100

    


    override fun onCreate() {
        super.onCreate()
        AssistantCore.init(applicationContext)
        startForegroundServiceNotification()
        setupFloatingView()
        
    }

    private fun startForegroundServiceNotification() {
        val channelId = "floating_assistant_channel"
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "Assistant Background Service",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            manager.createNotificationChannel(channel)
        }

        val notification = NotificationCompat.Builder(this, channelId)
            .setContentTitle("M.J Assistant")
            .setContentText("Running in background")
            .setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .build()
            
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            startForeground(1, notification, android.content.pm.ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE)
        } else {
            startForeground(1, notification)
        }
    }

    private fun setupFloatingView() {
        windowManager = getSystemService(WINDOW_SERVICE) as WindowManager
        
        val layoutFlag: Int = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            WindowManager.LayoutParams.TYPE_PHONE
        }

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            layoutFlag,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = paramsX
            y = paramsY
        }
        
        composeView = ComposeView(this).apply {
            setContent {
                MyApplicationTheme {
                    val state by AssistantCore.state.collectAsState()
                    val orbSize by AssistantCore.orbSizeFlow.collectAsState()
                    val orbTheme by AssistantCore.orbThemeFlow.collectAsState()
                    val isOrbVisible by AssistantCore.isOrbVisible.collectAsState()
                    
                    if (state != AssistantState.IDLE && state != AssistantState.ERROR && isOrbVisible) {
                        val displaySize = (120 * orbSize).dp
                        Box(
                            modifier = Modifier
                                .size(displaySize)
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxSize()
                                    .pointerInput(Unit) {
                                    detectDragGestures { change, dragAmount ->
                                        change.consume()
                                        paramsX += dragAmount.x.toInt()
                                        paramsY += dragAmount.y.toInt()
                                        params.x = paramsX
                                        params.y = paramsY
                                        windowManager.updateViewLayout(composeView, params)
                                    }
                                }
                                .pointerInput(Unit) {
                                    detectTapGestures(
                                        onTap = {
                                            val intent = Intent(this@FloatingService, com.example.MainActivity::class.java).apply {
                                                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
                                            }
                                            startActivity(intent)
                                        }
                                    )
                                }
                            ) {
                                com.example.ui.FloatingOrb(
                                    state = state,
                                    modifier = Modifier.fillMaxSize(),
                                    sizeMultiplier = 1f,
                                    themeIndex = orbTheme
                                )
                            }
                            
                            // Close button at top right
                            androidx.compose.material3.IconButton(
                                onClick = { AssistantCore.setOrbVisible(false) },
                                modifier = Modifier
                                    .align(androidx.compose.ui.Alignment.TopEnd)
                                    .size(24.dp)
                                    .background(androidx.compose.ui.graphics.Color.Black.copy(alpha = 0.5f), androidx.compose.foundation.shape.CircleShape)
                            ) {
                                androidx.compose.material3.Icon(
                                    imageVector = androidx.compose.material.icons.Icons.Default.Close,
                                    contentDescription = "Close",
                                    tint = androidx.compose.ui.graphics.Color.White,
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        }
                    }
                }
            }
        }

        lifecycleOwner.start()
        composeView.setViewTreeLifecycleOwner(lifecycleOwner)
        composeView.setViewTreeSavedStateRegistryOwner(lifecycleOwner)
        composeView.setViewTreeViewModelStoreOwner(lifecycleOwner)

        windowManager.addView(composeView, params)
    }

    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        return START_STICKY
    }

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onDestroy() {
        super.onDestroy()
        windowManager.removeView(composeView)
        lifecycleOwner.stop()

        

    }
}

class FloatingLifecycleOwner : SavedStateRegistryOwner, LifecycleOwner, ViewModelStoreOwner {
    private val lifecycleRegistry = LifecycleRegistry(this)
    private val savedStateRegistryController = SavedStateRegistryController.create(this)
    private val store = ViewModelStore()
    
    override val lifecycle: Lifecycle get() = lifecycleRegistry
    override val savedStateRegistry: SavedStateRegistry get() = savedStateRegistryController.savedStateRegistry
    override val viewModelStore: ViewModelStore get() = store

    fun start() {
        savedStateRegistryController.performRestore(null)
        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_CREATE)
        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_START)
        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_RESUME)
    }
    
    fun stop() {
        lifecycleRegistry.handleLifecycleEvent(Lifecycle.Event.ON_DESTROY)
        store.clear()
    }
}
