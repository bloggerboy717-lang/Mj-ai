import re

with open('app/src/main/java/com/example/audio/AudioPlayer.kt', 'r') as f:
    content = f.read()

content = content.replace("val bufferSize = AudioTrack.getMinBufferSize(sampleRate, channelConfig, audioFormat)", "val bufferSize = AudioTrack.getMinBufferSize(sampleRate, channelConfig, audioFormat) * 4")

# Update startPlaybackLoop
new_loop = """
    private fun startPlaybackLoop() {
        playbackJob = coroutineScope.launch {
            onPlaybackStateChanged(true)
            
            // Collect a few chunks before starting play to build a buffer and prevent stutter
            val initialChunks = mutableListOf<ByteArray>()
            repeat(4) {
                val data = audioQueue.receiveCatching().getOrNull()
                if (data != null) {
                    initialChunks.add(data)
                }
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
