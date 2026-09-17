import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace("sizeMultiplier = viewModel.getOrbSize(),", "sizeMultiplier = 1f, // App inner orb fixed size")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
