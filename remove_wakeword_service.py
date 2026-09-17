import re

with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

# Remove SpeechRecognizer initialization and related methods
methods_to_remove = r'private fun initWakeWordListener\(\) \{.*?(?=override fun onStartCommand)'
content = re.sub(methods_to_remove, '', content, flags=re.DOTALL)

content = content.replace("initWakeWordListener()", "")

# Remove variables
vars_to_remove = r'private var speechRecognizer: SpeechRecognizer\? = null.*?private val serviceScope = CoroutineScope\(Dispatchers\.Main\)'
content = re.sub(vars_to_remove, '', content, flags=re.DOTALL)

# Remove destroy
cleanup = r'speechRecognizer\?\.destroy\(\)\s*speechRecognizer = null'
content = re.sub(cleanup, '', content)

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(content)
