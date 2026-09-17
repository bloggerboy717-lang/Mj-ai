package com.example.audio

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import android.util.Base64
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch

class AudioPlayer(
    private val onPlaybackStateChanged: (Boolean) -> Unit
) {
    private var audioTrack: AudioTrack? = null
    private val coroutineScope = CoroutineScope(Dispatchers.IO)
    private val audioQueue = Channel<ByteArray>(Channel.UNLIMITED)
    private var playbackJob: Job? = null

    init {
        val sampleRate = 24000
        val channelConfig = AudioFormat.CHANNEL_OUT_MONO
        val audioFormat = AudioFormat.ENCODING_PCM_16BIT
        val bufferSize = AudioTrack.getMinBufferSize(sampleRate, channelConfig, audioFormat)

        audioTrack = AudioTrack.Builder()
            .setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build()
            )
            .setAudioFormat(
                AudioFormat.Builder()
                    .setEncoding(audioFormat)
                    .setSampleRate(sampleRate)
                    .setChannelMask(channelConfig)
                    .build()
            )
            .setBufferSizeInBytes(bufferSize)
            .setTransferMode(AudioTrack.MODE_STREAM)
            .build()
    }

    fun playAudioChunk(base64PcmData: String) {
        try {
            val pcmData = Base64.decode(base64PcmData, Base64.DEFAULT)
            audioQueue.trySend(pcmData)
            
            if (playbackJob == null || playbackJob?.isActive != true) {
                startPlaybackLoop()
            }
        } catch (e: Exception) {
            Log.e("AudioPlayer", "Error decoding or queueing audio", e)
        }
    }

    private fun startPlaybackLoop() {
        playbackJob = coroutineScope.launch {
            onPlaybackStateChanged(true)
            audioTrack?.play()
            
            while (isActive) {
                val data = audioQueue.receiveCatching().getOrNull()
                if (data != null) {
                    audioTrack?.write(data, 0, data.size)
                } else {
                    break
                }
                
                // If queue is empty, we stop spinning here and suspend on receive.
                // However, we want to know when we are done speaking.
                if (audioQueue.isEmpty) {
                    onPlaybackStateChanged(false)
                } else {
                    onPlaybackStateChanged(true)
                }
            }
        }
    }

    fun stopAndClearQueue() {
        playbackJob?.cancel()
        playbackJob = null
        // Drain queue
        while (!audioQueue.isEmpty) {
            audioQueue.tryReceive()
        }
        audioTrack?.pause()
        audioTrack?.flush()
        onPlaybackStateChanged(false)
    }

    fun release() {
        stopAndClearQueue()
        audioTrack?.release()
        audioTrack = null
    }
}
