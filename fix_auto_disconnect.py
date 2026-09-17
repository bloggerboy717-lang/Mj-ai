import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

# Make sure if we get an error we can see what it is
# Let's check the audio setup in AssistantCore.kt

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    core_content = f.read()

# Ensure we handle errors gracefully without auto cut.
