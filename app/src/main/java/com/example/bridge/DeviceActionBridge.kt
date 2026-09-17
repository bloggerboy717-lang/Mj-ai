package com.example.bridge

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.ContactsContract
import android.util.Log

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
}
