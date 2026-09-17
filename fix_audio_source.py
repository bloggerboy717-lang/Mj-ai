import re

with open('app/src/main/java/com/example/audio/AudioRecorder.kt', 'r') as f:
    content = f.read()

content = content.replace("MediaRecorder.AudioSource.VOICE_COMMUNICATION", "MediaRecorder.AudioSource.VOICE_RECOGNITION")
content = content.replace("MediaRecorder.AudioSource.MIC", "MediaRecorder.AudioSource.VOICE_RECOGNITION")

with open('app/src/main/java/com/example/audio/AudioRecorder.kt', 'w') as f:
    f.write(content)
