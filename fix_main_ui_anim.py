import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Add wakeWordInput state
if "var wakeWordInput" not in content:
    content = content.replace("var userNameInput by remember { mutableStateOf(viewModel.getUserName()) }", 
                              "var userNameInput by remember { mutableStateOf(viewModel.getUserName()) }\n    var wakeWordInput by remember { mutableStateOf(viewModel.getWakeWord()) }")

# 2. Add Wake Word TextField in Settings
wake_word_field = """
                    Spacer(modifier = Modifier.height(16.dp))
                    OutlinedTextField(
                        value = wakeWordInput,
                        onValueChange = { wakeWordInput = it },
                        label = { Text("Wake Word (e.g. AMJ)", color = Color.Gray) },
                        singleLine = true,
                        colors = androidx.compose.material3.OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = orangeAccent,
                            unfocusedBorderColor = Color.DarkGray,
                            focusedTextColor = Color.White,
                            unfocusedTextColor = Color.White
                        ),
                        shape = RoundedCornerShape(16.dp),
                        modifier = Modifier.fillMaxWidth()
                    )
"""
if "Wake Word" not in content:
    content = content.replace("viewModel.getUserName() },", "viewModel.getUserName() },\n" + wake_word_field)
    # wait, the replacement target is wrong. Let's find a better anchor.
    content = content.replace('label = { Text("Your Name", color = Color.Gray) },', 'label = { Text("Your Name", color = Color.Gray) },')
    # Let's use regex
    content = re.sub(r'(OutlinedTextField\([\s\S]*?label = \{ Text\("Your Name", color = Color\.Gray\) \},[\s\S]*?modifier = Modifier\.fillMaxWidth\(\)\n\s*\))', r'\1' + wake_word_field, content)


# 3. Save wake word
content = content.replace("viewModel.savePersona(personaInput)", "viewModel.savePersona(personaInput)\n                                viewModel.saveWakeWord(wakeWordInput)")

# 4. Open settings wake word init
content = content.replace("personaInput = viewModel.getPersona()", "personaInput = viewModel.getPersona()\n                                wakeWordInput = viewModel.getWakeWord()")

# 5. Animate Title (M.J) and Sky Blue color
title_pattern = r'Text\(\n\s*text = "M\.J",\n\s*style = MaterialTheme\.typography\.displayMedium,\n\s*fontWeight = FontWeight\.Bold,\n\s*color = Color\(0xFF8B2196\),\n\s*modifier = Modifier\n\s*\.align\(Alignment\.TopCenter\)\n\s*\.padding\(top = 64\.dp\)\n\s*\)'

animated_title = """
        val infiniteTransitionTitle = rememberInfiniteTransition(label = "title_anim")
        val titleScale by infiniteTransitionTitle.animateFloat(
            initialValue = 0.95f,
            targetValue = 1.05f,
            animationSpec = infiniteRepeatable(
                animation = tween(1500, easing = FastOutSlowInEasing),
                repeatMode = RepeatMode.Reverse
            ),
            label = "title_scale"
        )
        val titleAlpha by infiniteTransitionTitle.animateFloat(
            initialValue = 0.7f,
            targetValue = 1f,
            animationSpec = infiniteRepeatable(
                animation = tween(1500, easing = FastOutSlowInEasing),
                repeatMode = RepeatMode.Reverse
            ),
            label = "title_alpha"
        )

        Text(
            text = "M.J",
            style = MaterialTheme.typography.displayMedium,
            fontWeight = FontWeight.Bold,
            color = Color(0xFF00BFFF), // Sky Blue Color
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(top = 64.dp)
                .scale(titleScale)
                .alpha(titleAlpha)
        )
"""
content = re.sub(title_pattern, animated_title, content)


# 6. Animate Bottom Tab Bar
tab_bar_pattern = r'// Pill Background\n\s*Row\(\n\s*modifier = Modifier\n\s*\.width\(280\.dp\)\n\s*\.height\(64\.dp\)\n\s*\.background\(Color\(0xFFE0B877\), RoundedCornerShape\(32\.dp\)\),'

animated_tab_bar = """// Pill Background
                val infiniteTransitionTab = rememberInfiniteTransition(label = "tab_anim")
                val tabScale by infiniteTransitionTab.animateFloat(
                    initialValue = 0.98f,
                    targetValue = 1.02f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(2000, easing = LinearOutSlowInEasing),
                        repeatMode = RepeatMode.Reverse
                    ),
                    label = "tab_scale"
                )
                
                Row(
                    modifier = Modifier
                        .width(280.dp)
                        .height(64.dp)
                        .scale(tabScale)
                        .background(Color(0xFFE0B877), RoundedCornerShape(32.dp)),"""

content = re.sub(tab_bar_pattern, animated_tab_bar, content)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
