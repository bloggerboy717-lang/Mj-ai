import re
with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

content = content.replace("initWakeWordListener()\n        initWakeWordListener()", "initWakeWordListener()")

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(content)
