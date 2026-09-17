import re

with open('app/src/main/java/com/example/audio/AudioRecorder.kt', 'r') as f:
    content = f.read()

new_recording = """
    @SuppressLint("MissingPermission")
    fun startRecording() {
        try {
            val sampleRate = 16000
            val channelConfig = AudioFormat.CHANNEL_IN_MONO
            val audioFormat = AudioFormat.ENCODING_PCM_16BIT
            val bufferSize = AudioRecord.getMinBufferSize(sampleRate, channelConfig, audioFormat) * 2
            
            audioRecord = AudioRecord(
                MediaRecorder.AudioSource.VOICE_RECOGNITION,
                sampleRate,
                channelConfig,
                audioFormat,
                bufferSize
            )
            
            audioRecord?.startRecording()
            
            recordingJob = coroutineScope.launch {
                val buffer = ByteArray(bufferSize)
                while (isActive) {
                    val readResult = audioRecord?.read(buffer, 0, buffer.size) ?: 0
                    if (readResult > 0) {
                        val validData = buffer.copyOf(readResult)
                        val base64Data = Base64.encodeToString(validData, Base64.NO_WRAP)
                        onAudioReady(base64Data)
                    } else {
                        // If we read <= 0, something is wrong, we shouldn't spam the CPU
                        kotlinx.coroutines.delay(10)
                    }
                }
            }
        } catch (e: Exception) {
            android.util.Log.e("AudioRecorder", "Failed to start recording", e)
        }
    }
"""

content = re.sub(r'    @SuppressLint\("MissingPermission"\)\n    fun startRecording\(\) \{[\s\S]*?\}\s*\}\s*fun stopRecording', new_recording + '\n    fun stopRecording', content)

with open('app/src/main/java/com/example/audio/AudioRecorder.kt', 'w') as f:
    f.write(content)
