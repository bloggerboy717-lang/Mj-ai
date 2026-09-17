import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Locate the Box holding the controls
pattern = re.compile(r'Box\(\s*modifier = Modifier\.fillMaxWidth\(\)\.height\(120\.dp\),\s*contentAlignment = Alignment\.Center\s*\)\s*\{.*?(?=Spacer\(modifier = Modifier\.height\(16\.dp\)\))', re.DOTALL)

new_row = """Row(
                modifier = Modifier.fillMaxWidth().height(120.dp),
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(
                    onClick = {
                        apiKeyInput = viewModel.getApiKey()
                        elevenLabsKeyInput = viewModel.getElevenLabsKey()
                        userNameInput = viewModel.getUserName()
                        personaInput = viewModel.getPersona()
                        orbSizeInput = viewModel.getOrbSize()
                        orbThemeInput = viewModel.getOrbTheme()
                        showSettings = true
                    }
                ) {
                    Icon(
                        imageVector = Icons.Default.SettingsIcon,
                        contentDescription = "Settings",
                        tint = Color.White,
                        modifier = Modifier.size(32.dp)
                    )
                }
                
                Spacer(modifier = Modifier.width(32.dp))

                MicrophoneButton(
                    state = state,
                    onClick = onMicrophoneClick
                )
                
                Spacer(modifier = Modifier.width(32.dp))
                
                IconButton(
                    onClick = { showChat = true }
                ) {
                    Icon(
                        imageVector = Icons.Default.Chat,
                        contentDescription = "Chat",
                        tint = Color.White,
                        modifier = Modifier.size(32.dp)
                    )
                }
            }

            """

content = pattern.sub(new_row, content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
