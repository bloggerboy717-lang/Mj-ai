with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

if 'import androidx.compose.material.icons.filled.Close' not in text:
    text = text.replace('import androidx.compose.material.icons.filled.Chat', 'import androidx.compose.material.icons.filled.Chat\nimport androidx.compose.material.icons.filled.Close')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
