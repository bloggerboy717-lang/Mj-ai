import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add to Settings Dialog at the bottom
settings_bottom = r'Spacer\(modifier = Modifier\.height\(32\.dp\)\)\s*\}\s*\}\s*\}'
dev_text = """                    Spacer(modifier = Modifier.height(16.dp))
                    Text("Developer: Rohit Sir", color = Color.Gray, fontSize = 14.sp, modifier = Modifier.align(Alignment.CenterHorizontally))
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
        }"""
content = re.sub(settings_bottom, dev_text, content)

# Also add to the main screen bottom below the chat/settings buttons
bottom_row = r'label = "tab_scale"\s*\)\s*Row\(\s*modifier = Modifier'
dev_text_main = """label = "tab_scale"
                )
                
                Text("Developer: Rohit Sir", color = Color.Gray, fontSize = 12.sp, modifier = Modifier.padding(bottom = 8.dp))
                
                Row(
                    modifier = Modifier"""
content = re.sub(bottom_row, dev_text_main, content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
