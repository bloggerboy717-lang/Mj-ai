import re

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'r') as f:
    content = f.read()

content = content.replace('data class SetupComplete(val placeholder: String? = null)', 'class SetupComplete')
content = content.replace('val setupComplete: SetupComplete? = null', 'val setupComplete: Map<String, Any>? = null')

with open('app/src/main/java/com/example/gemini/GeminiModels.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

# Add a check for isUserRequestedDisconnect when receiving setupComplete so we don't start recording if we are disconnecting.
content = content.replace('Log.d("AssistantCore", "Setup complete received, starting audio recording")', 'Log.d("AssistantCore", "Setup complete received")\n                    if (isUserRequestedDisconnect) return@collect')

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
