import re

with open('app/src/main/java/com/example/audio/AudioPlayer.kt', 'r') as f:
    content = f.read()

# Let's add a small buffer mechanism
new_loop = """
    private fun startPlaybackLoop() {
        playbackJob = coroutineScope.launch {
            onPlaybackStateChanged(true)
            audioTrack?.play()
            
            // Wait until we have at least 2 chunks to prevent immediate underrun stutter
            var initialBuffer = 0
            while(initialBuffer < 2 && isActive) {
                kotlinx.coroutines.delay(50)
                initialBuffer++
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
