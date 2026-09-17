import re

with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

old_compose = """                MyApplicationTheme {
                    val state by AssistantCore.state.collectAsState()
                    
                    if (state != AssistantState.IDLE && state != AssistantState.ERROR) {
                        Box(
                            modifier = Modifier
                                .size(120.dp)"""
new_compose = """                MyApplicationTheme {
                    val state by AssistantCore.state.collectAsState()
                    val orbSize by AssistantCore.orbSizeFlow.collectAsState()
                    val orbTheme by AssistantCore.orbThemeFlow.collectAsState()
                    
                    if (state != AssistantState.IDLE && state != AssistantState.ERROR) {
                        val displaySize = (120 * orbSize).dp
                        Box(
                            modifier = Modifier
                                .size(displaySize)"""
content = content.replace(old_compose, new_compose)

old_orb_call = """                            com.example.ui.FloatingOrb(
                                state = state,
                                modifier = Modifier.fillMaxSize(),
                                sizeMultiplier = AssistantCore.getOrbSize(),
                                themeIndex = AssistantCore.getOrbTheme()
                            )"""
new_orb_call = """                            com.example.ui.FloatingOrb(
                                state = state,
                                modifier = Modifier.fillMaxSize(),
                                sizeMultiplier = 1f,
                                themeIndex = orbTheme
                            )"""
content = content.replace(old_orb_call, new_orb_call)

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(content)
