import re

with open('app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

assistant_services = """
        <service android:name=".service.MyRecognitionService"
            android:exported="true">
            <intent-filter>
                <action android:name="android.speech.RecognitionService" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </service>

        <service android:name=".service.MyVoiceInteractionService"
            android:permission="android.permission.BIND_VOICE_INTERACTION"
            android:exported="true">
            <meta-data android:name="android.voice_interaction"
                android:resource="@xml/voice_interaction_service" />
            <intent-filter>
                <action android:name="android.service.voice.VoiceInteractionService" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </service>

        <service android:name=".service.MyVoiceInteractionSessionService"
            android:permission="android.permission.BIND_VOICE_INTERACTION"
            android:exported="true">
            <intent-filter>
                <action android:name="android.service.voice.VoiceInteractionSessionService" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </service>
"""

if "MyVoiceInteractionService" not in content:
    content = content.replace("</application>", assistant_services + "\n    </application>")
    with open('app/src/main/AndroidManifest.xml', 'w') as f:
        f.write(content)
