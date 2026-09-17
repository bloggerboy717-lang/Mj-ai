import re

with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

content = content.replace("delay(500)\n                            startWakeWordListening()", "delay(2000)\n                            startWakeWordListening()")

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(content)
