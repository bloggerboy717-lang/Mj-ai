import re

with open('app/src/main/java/com/example/ui/FloatingOrb.kt', 'r') as f:
    content = f.read()

content = content.replace("val dotRadius = 6f + depth * 12f", "val dotRadius = 3.5f + depth * 7f")

with open('app/src/main/java/com/example/ui/FloatingOrb.kt', 'w') as f:
    f.write(content)
