import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

bad_anim = """androidx.compose.animation.core.withSequence {
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
        }"""

good_anim = """
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
"""
content = content.replace(bad_anim, good_anim)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
