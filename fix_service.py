with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    text = f.read()

text = text.replace(
    'com.example.ui.FloatingOrb(\n                            state = state,\n                            modifier = Modifier.fillMaxSize()\n                        )',
    'com.example.ui.FloatingOrb(\n                            state = state,\n                            modifier = Modifier.fillMaxSize(),\n                            sizeMultiplier = AssistantCore.getOrbSize(),\n                            themeIndex = AssistantCore.getOrbTheme()\n                        )'
)

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(text)
