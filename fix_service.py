import re

with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

pattern = re.compile(r'\.setSmallIcon\(android\.R\.drawable\.ic_btn_speak_now\)\n\s*\.build\(\)\n\s*startForeground\(1, notification\)')
replacement = """.setSmallIcon(android.R.drawable.ic_btn_speak_now)
            .build()
            
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            startForeground(1, notification, android.content.pm.ServiceInfo.FOREGROUND_SERVICE_TYPE_MICROPHONE)
        } else {
            startForeground(1, notification)
        }"""
content = pattern.sub(replacement, content)

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(content)
