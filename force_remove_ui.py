import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = re.sub(r'\s*Text\("Developer: Rohit Sir"[^\)]*\)', '', content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
