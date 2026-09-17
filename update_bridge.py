import re

with open('app/src/main/java/com/example/bridge/DeviceActionBridge.kt', 'r') as f:
    content = f.read()

imports_to_add = """import android.os.BatteryManager
import android.os.Build
import android.app.ActivityManager
import org.json.JSONObject
import java.net.URL
"""

content = content.replace('import android.util.Log', 'import android.util.Log\n' + imports_to_add)

new_functions = """
    fun getDeviceDetails(): Map<String, String> {
        try {
            val bm = context.getSystemService(Context.BATTERY_SERVICE) as BatteryManager
            val batteryLevel = bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
            
            val am = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
            val memoryInfo = ActivityManager.MemoryInfo()
            am.getMemoryInfo(memoryInfo)
            val totalRamGb = memoryInfo.totalMem / (1024 * 1024 * 1024.0)
            
            return mapOf(
                "brand" to Build.BRAND,
                "model" to Build.MODEL,
                "os_version" to Build.VERSION.RELEASE,
                "battery_percent" to batteryLevel.toString(),
                "total_ram_gb" to String.format("%.1f", totalRamGb)
            )
        } catch (e: Exception) {
            Log.e("DeviceActionBridge", "Error getting device details", e)
            return mapOf("error" to "Could not get device details")
        }
    }

    fun getLocation(): Map<String, String> {
        return try {
            // Use IP-API to get rough location based on IP. This is quick and requires no permissions.
            val response = URL("http://ip-api.com/json/").readText()
            val json = JSONObject(response)
            if (json.getString("status") == "success") {
                mapOf(
                    "city" to json.getString("city"),
                    "region" to json.getString("regionName"),
                    "country" to json.getString("country"),
                    "lat" to json.getDouble("lat").toString(),
                    "lon" to json.getDouble("lon").toString()
                )
            } else {
                mapOf("error" to "Location API failed")
            }
        } catch (e: Exception) {
            Log.e("DeviceActionBridge", "Error getting location", e)
            mapOf("error" to "Network error getting location")
        }
    }

    fun getWeather(): Map<String, String> {
        return try {
            // wttr.in gives weather for the current IP automatically if no location is specified.
            val response = URL("https://wttr.in/?format=j1").readText()
            val json = JSONObject(response)
            val currentCondition = json.getJSONArray("current_condition").getJSONObject(0)
            val tempC = currentCondition.getString("temp_C")
            val desc = currentCondition.getJSONArray("weatherDesc").getJSONObject(0).getString("value")
            
            val area = json.getJSONArray("nearest_area").getJSONObject(0).getJSONArray("areaName").getJSONObject(0).getString("value")
            
            mapOf(
                "location" to area,
                "temperature_celsius" to tempC,
                "description" to desc
            )
        } catch (e: Exception) {
            Log.e("DeviceActionBridge", "Error getting weather", e)
            mapOf("error" to "Network error getting weather")
        }
    }
"""

content = content[:-1] + new_functions + "}\n"

with open('app/src/main/java/com/example/bridge/DeviceActionBridge.kt', 'w') as f:
    f.write(content)
