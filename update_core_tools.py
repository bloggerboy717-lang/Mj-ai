import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

new_tools = """                "callContact" -> {
                    val contactName = args?.get("contactName") ?: return mapOf("error" to "Missing contactName")
                    val phone = bridge.findContactNumber(contactName)
                    if (phone != null) {
                        val success = bridge.makeCall(phone)
                        mapOf("success" to success.toString(), "contactFound" to "true")
                    } else {
                        mapOf("error" to "Contact not found", "contactFound" to "false")
                    }
                }
                "getDeviceDetails" -> {
                    bridge.getDeviceDetails()
                }
                "getLocation" -> {
                    bridge.getLocation()
                }
                "getWeather" -> {
                    bridge.getWeather()
                }"""

content = re.sub(r'                "callContact" -> \{[\s\S]*?\}\n                else ->', new_tools + '\n                else ->', content)

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
