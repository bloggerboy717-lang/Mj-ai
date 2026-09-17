import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("import kotlinx.coroutines.launchimport kotlinx.coroutines.delay", "")
content = content.replace("package com.example", "package com.example\n\nimport kotlinx.coroutines.launch\nimport kotlinx.coroutines.delay")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
