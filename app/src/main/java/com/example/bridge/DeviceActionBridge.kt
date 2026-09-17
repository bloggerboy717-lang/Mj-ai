package com.example.bridge

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.ContactsContract
import android.util.Log
import android.os.BatteryManager
import android.os.Build
import android.app.ActivityManager
import org.json.JSONObject
import java.net.URL


class DeviceActionBridge(private val context: Context) {

    fun openWhatsApp(): Boolean {
        return try {
            val intent = context.packageManager.getLaunchIntentForPackage("com.whatsapp")
            if (intent != null) {
                context.startActivity(intent)
                true
            } else {
                Log.e("DeviceActionBridge", "WhatsApp not installed")
                false
            }
        } catch (e: Exception) {
            Log.e("DeviceActionBridge", "Error opening WhatsApp", e)
            false
        }
    }

    fun openApp(appName: String): Boolean {
        // Simple heuristic: check common packages
        val packageManager = context.packageManager
        val packages = packageManager.getInstalledApplications(0)
        
        val matchingApp = packages.firstOrNull { 
            packageManager.getApplicationLabel(it).toString().contains(appName, ignoreCase = true)
        }

        return if (matchingApp != null) {
            val intent = packageManager.getLaunchIntentForPackage(matchingApp.packageName)
            if (intent != null) {
                context.startActivity(intent)
                true
            } else {
                false
            }
        } else {
            false
        }
    }

    fun openUrl(url: String): Boolean {
        return try {
            var finalUrl = url
            if (!finalUrl.startsWith("http://") && !finalUrl.startsWith("https://")) {
                finalUrl = "https://\$finalUrl"
            }
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(finalUrl))
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
            context.startActivity(intent)
            true
        } catch (e: Exception) {
            Log.e("DeviceActionBridge", "Error opening URL", e)
            false
        }
    }

    fun makeCall(phoneNumber: String): Boolean {
        return try {
            val intent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:\$phoneNumber"))
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
            context.startActivity(intent)
            true
        } catch (e: Exception) {
            Log.e("DeviceActionBridge", "Error making call", e)
            false
        }
    }

    fun findContactNumber(contactName: String): String? {
        var phoneNumber: String? = null
        try {
            val cursor = context.contentResolver.query(
                ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                arrayOf(ContactsContract.CommonDataKinds.Phone.NUMBER),
                "\${ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME} LIKE ?",
                arrayOf("%\$contactName%"),
                null
            )
            
            cursor?.use {
                if (it.moveToFirst()) {
                    phoneNumber = it.getString(it.getColumnIndexOrThrow(ContactsContract.CommonDataKinds.Phone.NUMBER))
                }
            }
        } catch (e: Exception) {
            Log.e("DeviceActionBridge", "Error finding contact", e)
        }
        return phoneNumber
    }

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
            val response = URL("https://ipapi.co/json/").readText()
            val json = JSONObject(response)
            if (json.has("city")) {
                mapOf(
                    "city" to json.getString("city"),
                    "region" to json.getString("region"),
                    "country" to json.getString("country_name"),
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
}
