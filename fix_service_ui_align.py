import re

with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

content = content.replace('.androidx.compose.ui.Alignment.Companion.align(androidx.compose.ui.Alignment.TopEnd)', '.align(androidx.compose.ui.Alignment.TopEnd)')

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(content)
