package com.example.audio

import android.annotation.SuppressLint
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import android.util.Base64
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

class AudioRecorder(
    private val onAudioReady: (String) -> Unit
) {
    private var audioRecord: AudioRecord? = null
    private var recordingJob: Job? = null
    private val coroutineScope = CoroutineScope(Dispatchers.IO)


    @SuppressLint("MissingPermission")
    fun startRecording() {
        if (recordingJob?.isActive == true) return
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

    fun stopRecording() {
        recordingJob?.cancel()
        recordingJob = null
        audioRecord?.stop()
        audioRecord?.release()
        audioRecord = null
    }
}
