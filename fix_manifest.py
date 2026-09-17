import re

with open('app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

content = content.replace('<uses-permission android:name="android.permission.INTERNET" />', '<uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.QUERY_ALL_PACKAGES" />')

with open('app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)
