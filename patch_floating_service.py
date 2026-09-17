import re

with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

# Read the new state
old_states = """                    val state by AssistantCore.state.collectAsState()
                    val orbSize by AssistantCore.orbSizeFlow.collectAsState()
                    val orbTheme by AssistantCore.orbThemeFlow.collectAsState()"""

new_states = """                    val state by AssistantCore.state.collectAsState()
                    val orbSize by AssistantCore.orbSizeFlow.collectAsState()
                    val orbTheme by AssistantCore.orbThemeFlow.collectAsState()
                    val isOrbVisible by AssistantCore.isOrbVisible.collectAsState()"""

content = content.replace(old_states, new_states)

# Add visibility check
old_if = "if (state != AssistantState.IDLE && state != AssistantState.ERROR) {"
new_if = "if (state != AssistantState.IDLE && state != AssistantState.ERROR && isOrbVisible) {"
content = content.replace(old_if, new_if)

# Change the close button logic
old_close = "onClick = { AssistantCore.disconnect() }"
new_close = "onClick = { AssistantCore.setOrbVisible(false) }"
content = content.replace(old_close, new_close)

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(content)
