import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# 1. Background color
content = content.replace("Color(0xFF5C5A56)", "Color.Black")

# 2. Add splash screen logic in onCreate
splash_logic = """
        setContent {
            MyApplicationTheme {
                var currentScreen by remember { mutableStateOf("splash") }

                if (currentScreen == "splash") {
                    SplashScreen(onTimeout = { currentScreen = "assistant" })
                } else {
                    Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                        AssistantScreen(
                            viewModel = viewModel,
                            modifier = Modifier.padding(innerPadding),
                            onMicrophoneClick = { checkPermissionsAndToggle() }
                        )
                    }
                }
            }
        }
"""
content = re.sub(r'setContent\s*\{\s*MyApplicationTheme\s*\{\s*Scaffold.*?\}\s*\}\s*\}', splash_logic, content, flags=re.DOTALL)

# 3. Add SplashScreen composable at the end
splash_composable = """

@Composable
fun SplashScreen(onTimeout: () -> Unit) {
    val scale = remember { androidx.compose.animation.core.Animatable(0.5f) }
    val alpha = remember { androidx.compose.animation.core.Animatable(0f) }
    
    LaunchedEffect(Unit) {
        // "Dangerous" / Awesome animation
        androidx.compose.animation.core.withSequence {
            androidx.compose.animation.core.coroutineScope {
                kotlinx.coroutines.launch {
                    scale.animateTo(
                        targetValue = 1.2f,
                        animationSpec = tween(1200, easing = FastOutSlowInEasing)
                    )
                    scale.animateTo(
                        targetValue = 1f,
                        animationSpec = tween(500, easing = LinearOutSlowInEasing)
                    )
                }
                kotlinx.coroutines.launch {
                    alpha.animateTo(
                        targetValue = 1f,
                        animationSpec = tween(1000)
                    )
                }
            }
        }
        kotlinx.coroutines.delay(1000)
        onTimeout()
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black),
        contentAlignment = Alignment.Center
    ) {
        androidx.compose.foundation.Image(
            painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.app_logo),
            contentDescription = "App Logo",
            modifier = Modifier
                .size(250.dp)
                .scale(scale.value)
                .alpha(alpha.value)
        )
    }
}
"""
content = content + splash_composable

# Also fix the imports if needed (import androidx.compose.ui.draw.alpha)
if "import androidx.compose.ui.draw.alpha" not in content:
    content = content.replace("import androidx.compose.ui.draw.scale", "import androidx.compose.ui.draw.scale\nimport androidx.compose.ui.draw.alpha")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
