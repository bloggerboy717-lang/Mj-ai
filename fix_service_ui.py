import re

with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

# Add a close button to the top right of the orb in the floating window
old_compose = """                    if (state != AssistantState.IDLE && state != AssistantState.ERROR) {
                        val displaySize = (120 * orbSize).dp
                        Box(
                            modifier = Modifier
                                .size(displaySize)
                                .pointerInput(Unit) {"""

new_compose = """                    if (state != AssistantState.IDLE && state != AssistantState.ERROR) {
                        val displaySize = (120 * orbSize).dp
                        Box(
                            modifier = Modifier
                                .size(displaySize)
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxSize()
                                    .pointerInput(Unit) {"""

content = content.replace(old_compose, new_compose)

old_orb_call = """                                }
                        ) {
                            com.example.ui.FloatingOrb(
                                state = state,
                                modifier = Modifier.fillMaxSize(),
                                sizeMultiplier = 1f,
                                themeIndex = orbTheme
                            )
                        }"""

new_orb_call = """                                }
                            ) {
                                com.example.ui.FloatingOrb(
                                    state = state,
                                    modifier = Modifier.fillMaxSize(),
                                    sizeMultiplier = 1f,
                                    themeIndex = orbTheme
                                )
                            }
                            
                            // Close button at top right
                            androidx.compose.material3.IconButton(
                                onClick = { AssistantCore.disconnect() },
                                modifier = Modifier
                                    .androidx.compose.ui.Alignment.Companion.align(androidx.compose.ui.Alignment.TopEnd)
                                    .size(24.dp)
                                    .androidx.compose.foundation.background(androidx.compose.ui.graphics.Color.Black.copy(alpha = 0.5f), androidx.compose.foundation.shape.CircleShape)
                            ) {
                                androidx.compose.material3.Icon(
                                    imageVector = androidx.compose.material.icons.Icons.Default.Close,
                                    contentDescription = "Close",
                                    tint = androidx.compose.ui.graphics.Color.White,
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        }"""
content = content.replace(old_orb_call, new_orb_call)

# Add missing imports
imports = """import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.foundation.background
import androidx.compose.foundation.shape.CircleShape
"""
content = content.replace("import androidx.compose.ui.unit.dp\n", "import androidx.compose.ui.unit.dp\n" + imports)

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(content)

