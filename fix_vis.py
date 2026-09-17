import re

with open('app/src/main/java/com/example/service/VoiceInteractionServices.kt', 'r') as f:
    content = f.read()

good_show = """    override fun onShow(args: Bundle?, showFlags: Int) {
        super.onShow(args, showFlags)
        val intent = Intent(context, com.example.MainActivity::class.java).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP)
        }
        context.startActivity(intent)
        
        // Start assistant automatically
        if (com.example.core.AssistantCore.state.value == com.example.viewmodel.AssistantState.IDLE) {
            com.example.core.AssistantCore.toggleConnection()
        }
    }"""

content = re.sub(r'override fun onShow\([^}]+\}[^}]+}', good_show, content)

with open('app/src/main/java/com/example/service/VoiceInteractionServices.kt', 'w') as f:
    f.write(content)
