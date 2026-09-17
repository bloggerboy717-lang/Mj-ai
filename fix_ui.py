import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Update background color
content = content.replace("Color(0xFFFFF0E6)", "Color(0xFF5C5A56)")

# 2. Update title color
content = re.sub(r'text = "M\.J",\n\s*style = MaterialTheme\.typography\.displayMedium,\n\s*fontWeight = FontWeight\.Bold,\n\s*color = orangeAccent,', 
                 'text = "M.J",\n            style = MaterialTheme.typography.displayMedium,\n            fontWeight = FontWeight.Bold,\n            color = Color(0xFF8B2196),', content)

# 3. Always show ORB
orb_pattern = r'// Show ORB only when microphone is listening/speaking/connecting\n\s*if \(state != AssistantState\.IDLE && state != AssistantState\.ERROR\) \{\n\s*androidx\.compose\.foundation\.layout\.Box\(\n\s*modifier = Modifier\n\s*\.align\(Alignment\.Center\)\n\s*\.size\(250\.dp\)\n\s*\) \{\n\s*com\.example\.ui\.FloatingOrb\(\n\s*state = state,\n\s*modifier = Modifier\.fillMaxSize\(\),\n\s*sizeMultiplier = viewModel\.getOrbSize\(\),\n\s*themeIndex = viewModel\.getOrbTheme\(\)\n\s*\)\n\s*\}\n\s*\}'

orb_replacement = """// Show ORB always
        androidx.compose.foundation.layout.Box(
            modifier = Modifier
                .align(Alignment.Center)
                .size(250.dp)
        ) {
            com.example.ui.FloatingOrb(
                // Force LISTENING state so it always spins colorfully
                state = if (state == AssistantState.IDLE) AssistantState.LISTENING else state,
                modifier = Modifier.fillMaxSize(),
                sizeMultiplier = viewModel.getOrbSize(),
                themeIndex = viewModel.getOrbTheme()
            )
        }"""
content = re.sub(orb_pattern, orb_replacement, content, flags=re.DOTALL)

# 4. Status text color White
content = content.replace("color = Color.DarkGray", "color = Color.White")

# 5. Pill Background
content = content.replace("Color(0xFF1E1E1E)", "Color(0xFFE0B877)")

# 6. Buttons styling (Chat and Settings)
buttons_pattern = re.compile(r'// Chat Button \(Left\).*?// Mic Button overlapping', re.DOTALL)
new_buttons = """// Chat Button (Left)
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight()
                            .clickable { showChat = true },
                        contentAlignment = Alignment.Center
                    ) {
                        Column(
                            modifier = Modifier
                                .background(Color(0xFFD1A471), RoundedCornerShape(20.dp))
                                .padding(horizontal = 24.dp, vertical = 8.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Icon(Icons.Default.Chat, contentDescription = "Chat", tint = Color(0xFF5C5A56), modifier = Modifier.size(20.dp))
                            Text("Chat", color = Color(0xFF5C5A56), fontSize = 12.sp, fontWeight = FontWeight.Bold)
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
                            modifier = Modifier
                                .background(Color(0xFFD1A471), RoundedCornerShape(20.dp))
                                .padding(horizontal = 24.dp, vertical = 8.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Icon(Icons.Default.SettingsIcon, contentDescription = "Settings", tint = Color(0xFF5C5A56), modifier = Modifier.size(20.dp))
                            Text("Settings", color = Color(0xFF5C5A56), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }

                // Mic Button overlapping"""

content = buttons_pattern.sub(new_buttons, content)

# 7. Center Mic Button color -> orange (FFA500)
content = content.replace("val buttonColor = Color(0xFFFE7C22)", "val buttonColor = Color(0xFFFFA500)")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
