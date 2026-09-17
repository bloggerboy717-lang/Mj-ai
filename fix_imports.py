import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Fix imports before package
if content.startswith("import"):
    # Find package
    pkg_match = re.search(r'package com.example', content)
    if pkg_match:
        # Move package to the top
        content = re.sub(r'import kotlin\.math\.roundToInt\nimport androidx\.compose\.foundation\.layout\.offset\npackage com\.example', 'package com.example\nimport kotlin.math.roundToInt\nimport androidx.compose.foundation.layout.offset\nimport androidx.compose.ui.input.pointer.pointerInput\nimport androidx.compose.foundation.gestures.detectDragGestures\n', content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
