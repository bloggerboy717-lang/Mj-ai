import re

with open('app/src/main/java/com/example/audio/AudioPlayer.kt', 'r') as f:
    content = f.read()

new_loop = """
    private fun startPlaybackLoop() {
        playbackJob = coroutineScope.launch {
            onPlaybackStateChanged(true)
            
            // Collect chunks for a short time to build a buffer and prevent stutter
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
            }
            
            audioTrack?.play()
            
            // Write initial buffered chunks
            for (data in initialChunks) {
                audioTrack?.write(data, 0, data.size)
            }

            while (isActive) {
                val data = audioQueue.receiveCatching().getOrNull()
                if (data != null) {
                    audioTrack?.write(data, 0, data.size)
                } else {
                    break
                }
                
                if (audioQueue.isEmpty) {
                    onPlaybackStateChanged(false)
                } else {
                    onPlaybackStateChanged(true)
                }
            }
        }
    }
"""

content = re.sub(r'private fun startPlaybackLoop\(\) \{[\s\S]*?\}\s*\}\s*fun stopAndClearQueue', new_loop + '\n    fun stopAndClearQueue', content)

with open('app/src/main/java/com/example/audio/AudioPlayer.kt', 'w') as f:
    f.write(content)
