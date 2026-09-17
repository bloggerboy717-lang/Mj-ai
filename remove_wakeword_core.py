import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

# Remove methods
methods = r'fun getWakeWord\(\): String \{[\s\S]*?fun saveWakeWord\(word: String\) \{[\s\S]*?\}\s*'
content = re.sub(methods, '', content)

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/viewmodel/AssistantViewModel.kt', 'r') as f:
    content = f.read()

# Remove methods
methods_vm = r'fun getWakeWord\(\): String = AssistantCore\.getWakeWord\(\)\s*fun saveWakeWord\(word: String\) = AssistantCore\.saveWakeWord\(word\)\s*'
content = re.sub(methods_vm, '', content)

with open('app/src/main/java/com/example/viewmodel/AssistantViewModel.kt', 'w') as f:
    f.write(content)
