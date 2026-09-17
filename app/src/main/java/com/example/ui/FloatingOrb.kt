package com.example.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import com.example.viewmodel.AssistantState
import kotlin.math.*

@Composable
fun FloatingOrb(state: AssistantState, modifier: Modifier = Modifier, sizeMultiplier: Float = 1f, themeIndex: Int = 0) {
    val infiniteTransition = rememberInfiniteTransition(label = "orb_rotation")
    
    // Spin speed depends on state
    val spinDuration = when(state) {
        AssistantState.SPEAKING -> 2000
        AssistantState.LISTENING -> 3000
        AssistantState.CONNECTING -> 1000
        else -> 8000
    }
    
    val rotation by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 2f * PI.toFloat(),
        animationSpec = infiniteRepeatable(
            animation = tween(spinDuration, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "spin"
    )

    Canvas(modifier = modifier.fillMaxSize()) {
        val radius = (size.minDimension / 2.2f) * sizeMultiplier
        val center = Offset(size.width / 2, size.height / 2)
        val numPoints = 250 // Many small dots
        val phi = PI * (3 - sqrt(5.0))

        for (i in 0 until numPoints) {
            val y = 1f - (i / (numPoints - 1f)) * 2f
            val r = sqrt(1.0 - y * y).toFloat()
            val theta = (phi * i).toFloat() + rotation

            val x = cos(theta) * r
            val z = sin(theta) * r

            // Tilt slightly to make it look 3D (similar to image)
            val tilt = PI / 5
            val yRot = (y * cos(tilt) - z * sin(tilt)).toFloat()
            val zRot = (y * sin(tilt) + z * cos(tilt)).toFloat()

            // Draw only front hemisphere + a bit of the back for depth
            if (zRot > -0.6f) {
                val screenX = center.x + x * radius
                val screenY = center.y + yRot * radius
                
                val depth = (zRot + 1f) / 2f // 0 to 1, where 1 is front
                val dotRadius = 1.5f + depth * 3f // small dots

                // Color mapped across the sphere to create a gradient
                val baseHue = when (themeIndex) {
                    0 -> 120f + x * 120f // Default Colorful
                    1 -> 15f + x * 20f   // Fire Orange
                    2 -> 200f + x * 20f  // Blue Ice
                    3 -> 120f + x * 10f  // Matrix Green
                    4 -> 280f + x * 20f  // Purple Magic
                    else -> 120f + x * 120f
                }
                
                val hue = (baseHue + yRot * 40f + rotation * 20f) % 360f
                val finalHue = if (hue < 0) hue + 360f else hue
                
                val saturation = if (themeIndex == 0) 0.85f else 0.95f
                val value = if (themeIndex == 0) 0.9f else 1.0f

                val hsvColor = android.graphics.Color.HSVToColor(
                    (0.3f + depth * 0.7f * 255).toInt(), 
                    floatArrayOf(finalHue, saturation, value)
                )

                drawCircle(
                    color = Color(hsvColor),
                    radius = dotRadius,
                    center = Offset(screenX, screenY)
                )
            }
        }
    }
}
