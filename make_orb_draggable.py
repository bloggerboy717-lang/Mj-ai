import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Make in-app orb draggable
# Find Box around FloatingOrb
orb_box_pattern = r'androidx\.compose\.foundation\.layout\.Box\(\n\s*modifier = Modifier\n\s*\.align\(Alignment\.Center\)\n\s*\.size\(250\.dp\)\n\s*\)'

new_orb_box = """
        var orbOffsetX by remember { mutableStateOf(0f) }
        var orbOffsetY by remember { mutableStateOf(0f) }
        
        androidx.compose.foundation.layout.Box(
            modifier = Modifier
                .align(Alignment.Center)
                .offset { androidx.compose.ui.unit.IntOffset(orbOffsetX.roundToInt(), orbOffsetY.roundToInt()) }
                .size(250.dp)
                .pointerInput(Unit) {
                    androidx.compose.foundation.gestures.detectDragGestures { change, dragAmount ->
                        change.consume()
                        orbOffsetX += dragAmount.x
                        orbOffsetY += dragAmount.y
                    }
                }
        )
"""

if "orbOffsetX" not in content:
    content = content.replace("androidx.compose.foundation.layout.Box(\n            modifier = Modifier\n                .align(Alignment.Center)\n                .size(250.dp)\n        )", new_orb_box)

    # ensure imports are there
    if "import kotlin.math.roundToInt" not in content:
        content = "import kotlin.math.roundToInt\nimport androidx.compose.foundation.layout.offset\n" + content

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
