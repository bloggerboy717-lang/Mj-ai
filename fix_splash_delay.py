import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("delay(1000)\n        onTimeout()", "delay(2000)\n        onTimeout()")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
