import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Remove UI state
content = re.sub(r'var wakeWordInput by remember \{ mutableStateOf\(viewModel\.getWakeWord\(\)\) \}\s*', '', content)

# Remove UI field
wakeword_field = r'Spacer\(modifier = Modifier\.height\(16\.dp\)\)\s*OutlinedTextField\(\s*value = wakeWordInput,[\s\S]*?modifier = Modifier\.fillMaxWidth\(\)\s*\)'
content = re.sub(wakeword_field, '', content)

# Remove save call
content = content.replace("viewModel.saveWakeWord(wakeWordInput)", "")

# Remove get call
content = content.replace("wakeWordInput = viewModel.getWakeWord()", "")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
