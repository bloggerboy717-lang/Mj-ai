import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

empty_params = ',\n                                parameters = Parameters(type = "OBJECT", properties = emptyMap())'

content = content.replace('description = "Get details about the user\'s phone/device like battery, model, RAM, etc."\n                            )', 'description = "Get details about the user\'s phone/device like battery, model, RAM, etc."' + empty_params + '\n                            )')
content = content.replace('description = "Get the user\'s current physical location (City, State, Country)."\n                            )', 'description = "Get the user\'s current physical location (City, State, Country)."' + empty_params + '\n                            )')
content = content.replace('description = "Get the current weather conditions for the user\'s location."\n                            )', 'description = "Get the current weather conditions for the user\'s location."' + empty_params + '\n                            )')
content = content.replace('description = "Open WhatsApp application"\n                            )', 'description = "Open WhatsApp application"' + empty_params + '\n                            )')

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
