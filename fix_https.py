import re

with open('app/src/main/java/com/example/bridge/DeviceActionBridge.kt', 'r') as f:
    content = f.read()

content = content.replace('http://ip-api.com/json/', 'https://ipapi.co/json/')
content = content.replace('json.getString("regionName")', 'json.getString("region")')
content = content.replace('json.getString("country")', 'json.getString("country_name")')
content = content.replace('json.getString("status") == "success"', 'json.has("city")')

with open('app/src/main/java/com/example/bridge/DeviceActionBridge.kt', 'w') as f:
    f.write(content)
