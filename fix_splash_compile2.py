import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("kotlinx.coroutines.launch", "launch")
content = content.replace("kotlinx.coroutines.delay", "kotlinx.coroutines.delay") # delay is fine, wait actually I'll just use delay() since I have import kotlinx.coroutines.* ? Actually, delay is a suspend function.

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
