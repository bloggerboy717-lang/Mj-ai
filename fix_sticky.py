import re

with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

on_start_command = """
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        return START_STICKY
    }
"""

if "onStartCommand" not in content:
    content = content.replace("override fun onBind", on_start_command + "\n    override fun onBind")
    with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
        f.write(content)
