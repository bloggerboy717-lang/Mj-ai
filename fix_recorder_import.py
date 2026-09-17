import re

with open('app/src/main/java/com/example/audio/AudioRecorder.kt', 'r') as f:
    content = f.read()

if "import kotlinx.coroutines.delay" not in content:
    content = content.replace("import kotlinx.coroutines.launch", "import kotlinx.coroutines.launch\nimport kotlinx.coroutines.delay")

with open('app/src/main/java/com/example/audio/AudioRecorder.kt', 'w') as f:
    f.write(content)
