import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

bad_start = """        if (Settings.canDrawOverlays(this)) {
            startFloatingService()
        }"""
        
good_start = """        if (Settings.canDrawOverlays(this) && ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
            startFloatingService()
        }"""
        
content = content.replace(bad_start, good_start)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
