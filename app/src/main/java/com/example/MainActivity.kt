package com.example

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.Chat
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Settings as SettingsIcon
import androidx.compose.material.icons.filled.Stop
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.example.service.FloatingService
import com.example.ui.theme.MyApplicationTheme
import com.example.viewmodel.AssistantState
import com.example.viewmodel.AssistantViewModel

class MainActivity : ComponentActivity() {

    private val viewModel: AssistantViewModel by viewModels()

    private val requestPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { permissions ->
            val audioGranted = permissions[Manifest.permission.RECORD_AUDIO] == true
            if (audioGranted) {
                checkOverlayPermissionAndStartService()
                viewModel.toggleConnection()
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    AssistantScreen(
                        viewModel = viewModel,
                        modifier = Modifier.padding(innerPadding),
                        onMicrophoneClick = { checkPermissionsAndToggle() }
                    )
                }
            }
        }
        
        // Start service if permission is already granted
        if (Settings.canDrawOverlays(this)) {
            startFloatingService()
        }
    }

    private fun checkOverlayPermissionAndStartService() {
        if (!Settings.canDrawOverlays(this)) {
            val intent = Intent(
                Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                Uri.parse("package:\$packageName")
            )
            startActivityForResult(intent, 1001)
        } else {
            startFloatingService()
        }
    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 1001) {
            if (Settings.canDrawOverlays(this)) {
                startFloatingService()
            }
        }
    }

    private fun startFloatingService() {
        val intent = Intent(this, FloatingService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
    }

    private fun checkPermissionsAndToggle() {
        val permissionsToRequest = mutableListOf(Manifest.permission.RECORD_AUDIO)
        
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
            permissionsToRequest.add(Manifest.permission.CALL_PHONE)
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) != PackageManager.PERMISSION_GRANTED) {
            permissionsToRequest.add(Manifest.permission.READ_CONTACTS)
        }
        
        // Post notifications for foreground service
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                permissionsToRequest.add(Manifest.permission.POST_NOTIFICATIONS)
            }
        }

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
            checkOverlayPermissionAndStartService()
            viewModel.toggleConnection()
        } else {
            requestPermissionLauncher.launch(permissionsToRequest.toTypedArray())
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AssistantScreen(
    viewModel: AssistantViewModel,
    modifier: Modifier = Modifier,
    onMicrophoneClick: () -> Unit
) {
    val state by viewModel.state.collectAsState()
    val error by viewModel.error.collectAsState()
    val chatMessages by viewModel.chatMessages.collectAsState()

    var showSettings by remember { mutableStateOf(false) }
    var showChat by remember { mutableStateOf(false) }
    
    var apiKeyInput by remember { mutableStateOf(viewModel.getApiKey()) }
    var elevenLabsKeyInput by remember { mutableStateOf(viewModel.getElevenLabsKey()) }
    var userNameInput by remember { mutableStateOf(viewModel.getUserName()) }
    var personaInput by remember { mutableStateOf(viewModel.getPersona()) }
    var orbSizeInput by remember { mutableStateOf(viewModel.getOrbSize()) }
    var orbThemeInput by remember { mutableStateOf(viewModel.getOrbTheme()) }

    val darkBg = Color(0xFF161616)
    val darkSurface = Color(0xFF252525)
    val orangeAccent = Color(0xFFFE7C22)

    val context = androidx.compose.ui.platform.LocalContext.current

    if (showSettings) {
        androidx.compose.ui.window.Dialog(onDismissRequest = { showSettings = false }, properties = androidx.compose.ui.window.DialogProperties(usePlatformDefaultWidth = false)) {
            Box(modifier = Modifier.fillMaxSize().background(darkBg).padding(24.dp)) {
                Column(modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState())) {
                    Text("Settings", style = MaterialTheme.typography.headlineMedium, color = Color.White, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    OutlinedTextField(
                        value = apiKeyInput,
                        onValueChange = { apiKeyInput = it },
                        label = { Text("Gemini API key", color = Color.Gray) },
                        singleLine = true,
                        colors = androidx.compose.material3.OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = orangeAccent,
                            unfocusedBorderColor = Color.DarkGray,
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White
                        ),
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier.fillMaxWidth()
                    )
                    androidx.compose.foundation.text.ClickableText(
                        text = androidx.compose.ui.text.AnnotatedString("How to get Gemini API key?"),
                        onClick = {
                            context.startActivity(Intent(Intent.ACTION_VIEW, android.net.Uri.parse("https://aistudio.google.com/app/apikey")))
                        },
                        style = androidx.compose.ui.text.TextStyle(color = orangeAccent, textDecoration = androidx.compose.ui.text.style.TextDecoration.Underline, fontSize = 12.sp),
                        modifier = Modifier.padding(start = 16.dp, top = 4.dp, bottom = 16.dp)
                    )

                    OutlinedTextField(
                        value = elevenLabsKeyInput,
                        onValueChange = { elevenLabsKeyInput = it },
                        label = { Text("ElevenLabs API key", color = Color.Gray) },
                        singleLine = true,
                        colors = androidx.compose.material3.OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = orangeAccent,
                            unfocusedBorderColor = Color.DarkGray,
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White
                        ),
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier.fillMaxWidth()
                    )
                    androidx.compose.foundation.text.ClickableText(
                        text = androidx.compose.ui.text.AnnotatedString("How to get ElevenLabs API key?"),
                        onClick = {
                            context.startActivity(Intent(Intent.ACTION_VIEW, android.net.Uri.parse("https://elevenlabs.io/api")))
                        },
                        style = androidx.compose.ui.text.TextStyle(color = orangeAccent, textDecoration = androidx.compose.ui.text.style.TextDecoration.Underline, fontSize = 12.sp),
                        modifier = Modifier.padding(start = 16.dp, top = 4.dp, bottom = 16.dp)
                    )

                    OutlinedTextField(
                        value = userNameInput,
                        onValueChange = { userNameInput = it },
                        label = { Text("Your name", color = Color.Gray) },
                        singleLine = true,
                        colors = androidx.compose.material3.OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = orangeAccent,
                            unfocusedBorderColor = Color.DarkGray,
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White
                        ),
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
                    )
                    
                    Text("Persona", style = MaterialTheme.typography.titleMedium, color = Color.White, modifier = Modifier.padding(bottom = 8.dp))
                    val personas = listOf("Friday", "Alic", "Darshan", "Piyush", "Pihu")
                    personas.forEach { p ->
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 4.dp).clickable { personaInput = p }) {
                            androidx.compose.material3.RadioButton(
                                selected = personaInput == p,
                                onClick = { personaInput = p },
                                colors = androidx.compose.material3.RadioButtonDefaults.colors(selectedColor = orangeAccent, unselectedColor = Color.Gray)
                            )
                            Text(p, color = Color.White, fontSize = 16.sp)
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))
                    Text("Orb Settings", style = MaterialTheme.typography.titleMedium, color = Color.White, modifier = Modifier.padding(bottom = 8.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("Size:", color = Color.White, modifier = Modifier.width(60.dp))
                        androidx.compose.material3.Slider(
                            value = orbSizeInput,
                            onValueChange = { orbSizeInput = it },
                            valueRange = 0.5f..2f,
                            colors = androidx.compose.material3.SliderDefaults.colors(thumbColor = orangeAccent, activeTrackColor = orangeAccent),
                            modifier = Modifier.weight(1f)
                        )
                    }
                    val themes = listOf("Colorful", "Fire", "Ice", "Matrix", "Purple")
                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.horizontalScroll(rememberScrollState())) {
                        Text("Theme:", color = Color.White, modifier = Modifier.padding(end = 8.dp))
                        themes.forEachIndexed { index, themeName ->
                            androidx.compose.material3.FilterChip(
                                selected = orbThemeInput == index,
                                onClick = { orbThemeInput = index },
                                label = { Text(themeName) },
                                colors = androidx.compose.material3.FilterChipDefaults.filterChipColors(selectedContainerColor = orangeAccent, selectedLabelColor = Color.White, labelColor = Color.Gray),
                                modifier = Modifier.padding(end = 4.dp)
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(32.dp))
                    Button(
                        onClick = {
                            context.startActivity(Intent(android.provider.Settings.ACTION_VOICE_INPUT_SETTINGS))
                        },
                        colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = orangeAccent),
                        shape = RoundedCornerShape(24.dp),
                        modifier = Modifier.fillMaxWidth().height(50.dp)
                    ) {
                        Text("Default AI assistant settings", color = Color.White)
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                        TextButton(onClick = { showSettings = false }) {
                            Text("Cancel", color = Color.White)
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Button(
                            onClick = {
                                viewModel.saveApiKey(apiKeyInput)
                                viewModel.saveElevenLabsKey(elevenLabsKeyInput)
                                viewModel.saveUserName(userNameInput)
                                viewModel.savePersona(personaInput)
                                viewModel.saveOrbSize(orbSizeInput)
                                viewModel.saveOrbTheme(orbThemeInput)
                                showSettings = false
                            },
                            colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = orangeAccent),
                            shape = RoundedCornerShape(24.dp)
                        ) {
                            Text("Save changes", color = Color.White)
                        }
                    }
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
        }
    }

    if (showChat) {
        androidx.compose.ui.window.Dialog(onDismissRequest = { showChat = false }, properties = androidx.compose.ui.window.DialogProperties(usePlatformDefaultWidth = false)) {
            Column(modifier = Modifier.fillMaxSize().background(darkBg)) {
                // Chat Header
                Row(modifier = Modifier.fillMaxWidth().background(darkBg).padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Box(modifier = Modifier.size(48.dp).background(orangeAccent, CircleShape), contentAlignment = Alignment.Center) {
                        Text("MJ", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    }
                    Spacer(modifier = Modifier.width(12.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text("M.J", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                        Text("online", color = Color.Gray, fontSize = 14.sp)
                    }
                    Box(modifier = Modifier.background(darkSurface, RoundedCornerShape(12.dp)).padding(horizontal = 12.dp, vertical = 4.dp)) {
                        Text("Pro", color = orangeAccent, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                    IconButton(onClick = { showChat = false }) {
                        Icon(androidx.compose.material.icons.Icons.Default.Close, contentDescription = "Close", tint = Color.Gray)
                    }
                }
                
                // Messages
                androidx.compose.foundation.lazy.LazyColumn(
                    modifier = Modifier.weight(1f).fillMaxWidth().padding(horizontal = 16.dp),
                    reverseLayout = true
                ) {
                    items(chatMessages.reversed()) { msg ->
                        val isUser = msg.isFromUser
                        val bubbleShape = if (isUser) {
                            RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp, bottomStart = 16.dp, bottomEnd = 4.dp)
                        } else {
                            RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp, bottomStart = 4.dp, bottomEnd = 16.dp)
                        }
                        val bgColor = if (isUser) orangeAccent else darkSurface
                        val textColor = Color.White

                        Box(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            contentAlignment = if (isUser) Alignment.CenterEnd else Alignment.CenterStart
                        ) {
                            Text(
                                text = msg.text,
                                modifier = Modifier
                                    .background(color = bgColor, shape = bubbleShape)
                                    .padding(16.dp)
                                    .widthIn(max = 280.dp),
                                color = textColor,
                                fontSize = 16.sp
                            )
                        }
                    }
                }
                
                // Input Area
                var chatInput by remember { mutableStateOf("") }
                Row(modifier = Modifier.fillMaxWidth().background(darkBg).padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    OutlinedTextField(
                        value = chatInput,
                        onValueChange = { chatInput = it },
                        modifier = Modifier.weight(1f),
                        placeholder = { Text("Message likhein", color = Color.Gray) },
                        colors = androidx.compose.material3.OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = darkSurface,
                            unfocusedContainerColor = darkSurface,
                            focusedBorderColor = Color.Transparent,
                            unfocusedBorderColor = Color.Transparent,
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White
                        ),
                        shape = RoundedCornerShape(24.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .background(orangeAccent, CircleShape)
                            .clickable {
                                if (chatInput.isNotBlank()) {
                                    viewModel.sendTextMessage(chatInput)
                                    chatInput = ""
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = Color.White)
                    }
                }
            }
        }
    }
    Box(
        modifier = modifier
            .fillMaxSize()
            .background(Color(0xFFFFF0E6)) // Very light orange background
    ) {
        Text(
            text = "M.J",
            style = MaterialTheme.typography.displayMedium,
            fontWeight = FontWeight.Bold,
            color = orangeAccent,
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(top = 64.dp)
        )

        // Show ORB only when microphone is listening/speaking/connecting
        if (state != AssistantState.IDLE && state != AssistantState.ERROR) {
            androidx.compose.foundation.layout.Box(
                modifier = Modifier
                    .align(Alignment.Center)
                    .size(250.dp)
            ) {
                com.example.ui.FloatingOrb(
                    state = state,
                    modifier = Modifier.fillMaxSize(),
                    sizeMultiplier = viewModel.getOrbSize(),
                    themeIndex = viewModel.getOrbTheme()
                )
            }
        }

        Column(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .padding(bottom = 32.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            if (error != null) {
                Text(
                    text = error ?: "",
                    color = MaterialTheme.colorScheme.error,
                    style = MaterialTheme.typography.labelMedium,
                    modifier = Modifier.padding(bottom = 16.dp, start = 32.dp, end = 32.dp),
                    textAlign = androidx.compose.ui.text.style.TextAlign.Center
                )
            }

            val statusText = when(state) {
                AssistantState.IDLE -> "Tab par tap karein"
                AssistantState.CONNECTING -> "Connecting to Gemini Live..."
                AssistantState.LISTENING -> "M.J is listening..."
                AssistantState.SPEAKING -> "M.J is speaking..."
                AssistantState.ERROR -> "Something went wrong"
            }
            Text(
                text = statusText,
                style = MaterialTheme.typography.bodyLarge,
                color = Color.DarkGray,
                fontWeight = FontWeight.Medium,
                modifier = Modifier.padding(bottom = 24.dp)
            )

            // Bottom Tab Bar
            Box(
                contentAlignment = Alignment.BottomCenter,
                modifier = Modifier.fillMaxWidth()
            ) {
                // Pill Background
                Row(
                    modifier = Modifier
                        .width(280.dp)
                        .height(64.dp)
                        .background(Color(0xFF1E1E1E), RoundedCornerShape(32.dp)),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    // Chat Button (Left)
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight()
                            .clickable { showChat = true },
                        contentAlignment = Alignment.Center
                    ) {
                        Column(
                            modifier = Modifier
                                .background(Color(0xFF332014), RoundedCornerShape(20.dp))
                                .padding(horizontal = 24.dp, vertical = 8.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Icon(Icons.Default.Chat, contentDescription = "Chat", tint = orangeAccent, modifier = Modifier.size(20.dp))
                            Text("Chat", color = orangeAccent, fontSize = 12.sp)
                        }
                    }

                    Spacer(modifier = Modifier.width(64.dp)) // Space for Mic

                    // Settings Button (Right)
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight()
                            .clickable {
                                apiKeyInput = viewModel.getApiKey()
                                elevenLabsKeyInput = viewModel.getElevenLabsKey()
                                userNameInput = viewModel.getUserName()
                                personaInput = viewModel.getPersona()
                                orbSizeInput = viewModel.getOrbSize()
                                orbThemeInput = viewModel.getOrbTheme()
                                showSettings = true
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Icon(Icons.Default.SettingsIcon, contentDescription = "Settings", tint = Color.Gray, modifier = Modifier.size(20.dp))
                            Text("Settings", color = Color.Gray, fontSize = 12.sp)
                        }
                    }
                }

                // Mic Button overlapping
                MicrophoneButton(
                    state = state,
                    onClick = onMicrophoneClick,
                    modifier = Modifier.offset(y = (-16).dp)
                )
            }
        }
    }
}

@Composable
fun MicrophoneButton(
    state: AssistantState,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val scale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = if (state == AssistantState.SPEAKING || state == AssistantState.LISTENING) 1.15f else 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulse_scale"
    )

    val buttonColor = Color(0xFFFE7C22)

    Box(
        modifier = modifier
            .size(80.dp)
            .scale(scale)
            .clip(CircleShape)
            .background(Color(0xFF151515)), 
        contentAlignment = Alignment.Center
    ) {
        Box(
            modifier = Modifier
                .size(60.dp)
                .clip(CircleShape)
                .background(buttonColor)
                .clickable { onClick() },
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = if (state == AssistantState.IDLE || state == AssistantState.ERROR) Icons.Default.Mic else Icons.Default.Stop,
                contentDescription = "Microphone",
                tint = Color.White,
                modifier = Modifier.size(32.dp)
            )
        }
    }
}
