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

class AudioRecorder(
    private val onAudioReady: (String) -> Unit
) {
    private var audioRecord: AudioRecord? = null
    private var recordingJob: Job? = null
    private val coroutineScope = CoroutineScope(Dispatchers.IO)

    @SuppressLint("MissingPermission")
    fun startRecording() {
        val sampleRate = 16000
        val channelConfig = AudioFormat.CHANNEL_IN_MONO
        val audioFormat = AudioFormat.ENCODING_PCM_16BIT
        val bufferSize = AudioRecord.getMinBufferSize(sampleRate, channelConfig, audioFormat) * 2

        audioRecord = AudioRecord(
            MediaRecorder.AudioSource.MIC,
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
                }
            }
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
