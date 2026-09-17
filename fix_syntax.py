import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("Spacer(modifier = Modifier.height(16.dp)))", "Spacer(modifier = Modifier.height(16.dp))")
content = content.replace("label = \"tab_scale\"\n                ))", "label = \"tab_scale\"\n                )")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
