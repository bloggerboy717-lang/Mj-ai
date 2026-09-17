import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

# Fix .sp.12.sp to 12.sp
text = re.sub(r'androidx\.compose\.ui\.unit\.sp\.(\d+)\.sp', r'\1.sp', text)

# Fix horizontalScroll import
if 'import androidx.compose.foundation.horizontalScroll' not in text:
    text = text.replace('import androidx.compose.foundation.layout.*', 'import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.horizontalScroll')

# Fix Close icon
text = text.replace('androidx.compose.material.icons.Icons.Default.Close', 'androidx.compose.material.icons.Icons.Default.Close') # wait, what was it? Icons.Default.Close. Let me add import for Close icon

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
