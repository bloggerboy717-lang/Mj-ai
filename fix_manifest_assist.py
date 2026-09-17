import re

with open('app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

# Fix MainActivity intent filters
main_activity_pattern = r'<intent-filter>\s*<action android:name="android.intent.action.MAIN" />\s*<category android:name="android.intent.category.LAUNCHER" />\s*</intent-filter>'
new_intent_filters = """<intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.ASSIST" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.VOICE_COMMAND" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>"""

content = re.sub(main_activity_pattern, new_intent_filters, content)

# Fix VoiceInteractionService to have label and icon
vis_pattern = r'<service android:name="\.service\.MyVoiceInteractionService"\s*android:permission="android\.permission\.BIND_VOICE_INTERACTION"\s*android:exported="true">'
new_vis = """<service android:name=".service.MyVoiceInteractionService"
            android:label="@string/app_name"
            android:icon="@drawable/app_logo"
            android:permission="android.permission.BIND_VOICE_INTERACTION"
            android:exported="true">"""

content = re.sub(vis_pattern, new_vis, content)

# Fix RecognitionService
rec_pattern = r'<service android:name="\.service\.MyRecognitionService"\s*android:exported="true">'
new_rec = """<service android:name=".service.MyRecognitionService"
            android:label="@string/app_name"
            android:icon="@drawable/app_logo"
            android:exported="true">"""

content = re.sub(rec_pattern, new_rec, content)

with open('app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)
