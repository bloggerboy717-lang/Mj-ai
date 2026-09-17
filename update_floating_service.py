import re

with open('app/src/main/java/com/example/service/FloatingService.kt', 'r') as f:
    content = f.read()

imports = """
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.os.Bundle
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay
import android.Manifest
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat
"""
if "android.speech.SpeechRecognizer" not in content:
    content = content.replace("import com.example.core.AssistantCore", imports + "import com.example.core.AssistantCore")


class_vars = """
    private var speechRecognizer: SpeechRecognizer? = null
    private var isListeningForWakeWord = false
    private val serviceScope = CoroutineScope(Dispatchers.Main)
"""

if "private var speechRecognizer" not in content:
    content = content.replace("private var paramsY = 100", "private var paramsY = 100\n" + class_vars)

init_method = """
    private fun initWakeWordListener() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            return
        }

        if (SpeechRecognizer.isRecognitionAvailable(this)) {
            speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
            speechRecognizer?.setRecognitionListener(object : RecognitionListener {
                override fun onReadyForSpeech(params: Bundle?) {}
                override fun onBeginningOfSpeech() {}
                override fun onRmsChanged(rmsdB: Float) {}
                override fun onBufferReceived(buffer: ByteArray?) {}
                override fun onEndOfSpeech() {}
                override fun onError(error: Int) {
                    isListeningForWakeWord = false
                    // Restart listening if still IDLE
                    if (AssistantCore.state.value == AssistantState.IDLE) {
                        serviceScope.launch {
                            delay(500)
                            startWakeWordListening()
                        }
                    }
                }

                override fun onResults(results: Bundle?) {
                    isListeningForWakeWord = false
                    val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                    val wakeWord = AssistantCore.getWakeWord().lowercase()
                    if (matches != null) {
                        for (match in matches) {
                            if (match.lowercase().contains(wakeWord)) {
                                Log.d("WakeWord", "Wake word detected!")
                                // Open App and Start Assistant
                                val intent = Intent(this@FloatingService, com.example.MainActivity::class.java).apply {
                                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
                                }
                                startActivity(intent)
                                
                                // Give it a slight delay to open the app
                                serviceScope.launch {
                                    delay(500)
                                    if (AssistantCore.state.value == AssistantState.IDLE) {
                                        AssistantCore.toggleConnection()
                                    }
                                }
                                return
                            }
                        }
                    }
                    // Restart if not detected
                    if (AssistantCore.state.value == AssistantState.IDLE) {
                        startWakeWordListening()
                    }
                }

                override fun onPartialResults(partialResults: Bundle?) {}
                override fun onEvent(eventType: Int, params: Bundle?) {}
            })
            
            // Observe state to start/stop
            serviceScope.launch {
                AssistantCore.state.collect { state ->
                    if (state == AssistantState.IDLE) {
                        startWakeWordListening()
                    } else {
                        stopWakeWordListening()
                    }
                }
            }
        }
    }

    private fun startWakeWordListening() {
        if (!isListeningForWakeWord && speechRecognizer != null && AssistantCore.state.value == AssistantState.IDLE) {
            val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, packageName)
                putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
            }
            try {
                speechRecognizer?.startListening(intent)
                isListeningForWakeWord = true
            } catch (e: Exception) {
                Log.e("WakeWord", "Failed to start listening", e)
            }
        }
    }

    private fun stopWakeWordListening() {
        if (isListeningForWakeWord && speechRecognizer != null) {
            speechRecognizer?.stopListening()
            isListeningForWakeWord = false
        }
    }
"""

if "initWakeWordListener" not in content:
    content = content.replace("setupFloatingView()", "setupFloatingView()\n        initWakeWordListener()")
    content = content.replace("override fun onBind", init_method + "\n    override fun onBind")

cleanup = """
        speechRecognizer?.destroy()
        speechRecognizer = null
"""

content = content.replace("lifecycleOwner.stop()", "lifecycleOwner.stop()\n" + cleanup)

with open('app/src/main/java/com/example/service/FloatingService.kt', 'w') as f:
    f.write(content)
