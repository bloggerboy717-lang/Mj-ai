import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Remove from Settings
settings_text = r'\s*Spacer\(modifier = Modifier\.height\(16\.dp\)\)\s*Text\("Developer: Rohit Sir"[^\)]*\)\s*Spacer\(modifier = Modifier\.height\(32\.dp\)\)'
content = re.sub(settings_text, '\n                    Spacer(modifier = Modifier.height(32.dp))', content)

# Remove from Main Screen
main_text = r'\s*Text\("Developer: Rohit Sir"[^\)]*\)\s*Row\('
content = re.sub(main_text, '\n                Row(', content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
