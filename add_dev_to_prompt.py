import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

old_instruction = 'Avoid explicit or inappropriate content while maintaining your charm, confidence, and personality."'
new_instruction = 'Avoid explicit or inappropriate content while maintaining your charm, confidence, and personality. Your developer and creator is Rohit Sir. If anyone asks who created you, who made you, or who your developer is, you must proudly answer that you were developed by Rohit Sir."'

content = content.replace(old_instruction, new_instruction)

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
