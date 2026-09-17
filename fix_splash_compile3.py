import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

if "import kotlinx.coroutines.launch" not in content:
    content = content.replace("import kotlinx.coroutines.*", "import kotlinx.coroutines.*\nimport kotlinx.coroutines.launch\nimport kotlinx.coroutines.delay")
    if "import kotlinx.coroutines.*" not in content:
        content = "import kotlinx.coroutines.launch\nimport kotlinx.coroutines.delay\n" + content

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
