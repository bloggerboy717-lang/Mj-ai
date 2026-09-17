import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

content = content.replace('"OBJECT"', '"object"').replace('"STRING"', '"string"')

tools_to_add = """                            FunctionDeclaration(
                                name = "getDeviceDetails",
                                description = "Get details about the user's phone/device like battery, model, RAM, etc."
                            ),
                            FunctionDeclaration(
                                name = "getLocation",
                                description = "Get the user's current physical location (City, State, Country)."
                            ),
                            FunctionDeclaration(
                                name = "getWeather",
                                description = "Get the current weather conditions for the user's location."
                            ),
                            FunctionDeclaration("""

content = content.replace('                            FunctionDeclaration(', tools_to_add, 1)

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
