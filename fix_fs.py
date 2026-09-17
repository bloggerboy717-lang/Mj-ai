import re
with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

content = content.replace("private fun setupFloatingView()\n        initWakeWordListener() {", "private fun setupFloatingView() {")
content = content.replace("setupFloatingView()", "setupFloatingView()\n        initWakeWordListener()", 1) # Only first occurrence (which should be in onCreate)

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(content)
