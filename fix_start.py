with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# find "import android.Manifest"
idx = content.find("import android.Manifest")
if idx != -1:
    content = "package com.example\n\nimport kotlinx.coroutines.launch\nimport kotlinx.coroutines.delay\n" + content[idx:]
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
