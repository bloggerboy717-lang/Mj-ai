import re

# Update AssistantCore.kt
with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    core_content = f.read()

wake_word_methods = """
    fun getWakeWord(): String {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        return prefs?.getString("wake_word", "Hey MJ") ?: "Hey MJ"
    }

    fun saveWakeWord(word: String) {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        prefs?.edit()?.putString("wake_word", word)?.apply()
    }
"""

if "getWakeWord" not in core_content:
    core_content = core_content.replace("fun getOrbSize(): Float {", wake_word_methods + "\n    fun getOrbSize(): Float {")
    with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
        f.write(core_content)


# Update AssistantViewModel.kt
with open('app/src/main/java/com/example/viewmodel/AssistantViewModel.kt', 'r') as f:
    vm_content = f.read()

vm_methods = """
    fun getWakeWord(): String = AssistantCore.getWakeWord()
    fun saveWakeWord(word: String) = AssistantCore.saveWakeWord(word)
"""

if "getWakeWord" not in vm_content:
    vm_content = vm_content.replace("fun getOrbSize(): Float =", vm_methods + "\n    fun getOrbSize(): Float =")
    with open('app/src/main/java/com/example/viewmodel/AssistantViewModel.kt', 'w') as f:
        f.write(vm_content)
