import re

with open('app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

assist_intent = """<intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            
            <!-- Added for Default Assistant Support -->
            <intent-filter>
                <action android:name="android.intent.action.ASSIST" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>"""

content = content.replace("""<intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>""", assist_intent)

with open('app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)
