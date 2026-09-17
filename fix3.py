with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

if 'import androidx.compose.ui.unit.sp' not in text:
    text = text.replace('import androidx.compose.ui.unit.dp', 'import androidx.compose.ui.unit.dp\nimport androidx.compose.ui.unit.sp')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
