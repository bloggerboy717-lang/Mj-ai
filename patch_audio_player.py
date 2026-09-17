import re

with open('app/src/main/java/com/example/audio/AudioPlayer.kt', 'r') as f:
    content = f.read()

# Increase buffer size in AudioTrack
old_buffer = "val bufferSize = AudioTrack.getMinBufferSize(sampleRate, channelConfig, audioFormat) * 4"
new_buffer = "val bufferSize = AudioTrack.getMinBufferSize(sampleRate, channelConfig, audioFormat) * 8 // Increased buffer for smooth playback"
content = content.replace(old_buffer, new_buffer)

# Increase initial chunks before playing
old_loop = """            // Collect chunks for a short time to build a buffer and prevent stutter
            val initialChunks = mutableListOf<ByteArray>()
            try {
                kotlinx.coroutines.withTimeout(500) {
                    while (initialChunks.size < 4 && isActive) {
                        val data = audioQueue.receiveCatching().getOrNull()
                        if (data != null) {
                            initialChunks.add(data)
                        } else {
                            break
                        }
                    }
                }
            } catch (e: Exception) {
                // Timeout reached, just proceed with what we have
            }"""

new_loop = """            // Build a solid buffer to prevent robotic stuttering
            val initialChunks = mutableListOf<ByteArray>()
            try {
                kotlinx.coroutines.withTimeout(800) {
                    while (initialChunks.size < 8 && isActive) {
                        val data = audioQueue.receiveCatching().getOrNull()
                        if (data != null) {
                            initialChunks.add(data)
                        } else {
                            break
                        }
                    }
                }
            } catch (e: Exception) {
                // Timeout reached
            }"""
content = content.replace(old_loop, new_loop)

with open('app/src/main/java/com/example/audio/AudioPlayer.kt', 'w') as f:
    f.write(content)
