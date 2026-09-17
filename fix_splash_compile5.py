with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.read().split('import')

content = []
for line in lines:
    line = line.strip()
    if line.startswith("kotlinx.coroutines.launch"): continue
    if line.startswith("kotlinx.coroutines.delay"): continue
    if line.startswith("package com.example"):
        content.append("package com.example\n\nimport kotlinx.coroutines.launch\nimport kotlinx.coroutines.delay")
    else:
        if line: content.append("import " + line)

# Rejoin
final_content = "\n".join(content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(final_content)
