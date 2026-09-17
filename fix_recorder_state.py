import re

with open('app/src/main/java/com/example/audio/AudioRecorder.kt', 'r') as f:
    content = f.read()

content = content.replace('    fun startRecording() {\n        try {', '    fun startRecording() {\n        if (recordingJob?.isActive == true) return\n        try {')

with open('app/src/main/java/com/example/audio/AudioRecorder.kt', 'w') as f:
    f.write(content)
