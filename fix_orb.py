import re

with open('app/src/main/java/com/example/ui/FloatingOrb.kt', 'r') as f:
    content = f.read()

# Make dots much bigger
content = content.replace("val dotRadius = 1.5f + depth * 3f", "val dotRadius = 6f + depth * 12f")

with open('app/src/main/java/com/example/ui/FloatingOrb.kt', 'w') as f:
    f.write(content)
