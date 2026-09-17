import re

with open('app/src/main/java/com/example/bridge/DeviceActionBridge.kt', 'r') as f:
    content = f.read()

# Fix the extra bracket
content = content.replace("        return phoneNumber\n    }\n}\n    fun getDeviceDetails()", "        return phoneNumber\n    }\n\n    fun getDeviceDetails()")
content = content.replace("        return phoneNumber\n    }\n}\n", "        return phoneNumber\n    }\n\n")

with open('app/src/main/java/com/example/bridge/DeviceActionBridge.kt', 'w') as f:
    f.write(content)
