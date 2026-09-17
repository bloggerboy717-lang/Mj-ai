import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

pattern_ui = re.compile(r'\s*Box\(\s*modifier = modifier\s*\.fillMaxSize\(\)\s*\.background\(Color\.Black\)\s*\)\s*\{.*', re.DOTALL)

replacement_ui = """
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
"""

content = pattern_ui.sub(replacement_ui, content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
