import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

# Add MutableStateFlows for orb size and theme
new_flows = """    private val _chatMessages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val chatMessages: StateFlow<List<ChatMessage>> = _chatMessages.asStateFlow()

    private val _orbSizeFlow = MutableStateFlow(1f)
    val orbSizeFlow: StateFlow<Float> = _orbSizeFlow.asStateFlow()

    private val _orbThemeFlow = MutableStateFlow(0)
    val orbThemeFlow: StateFlow<Int> = _orbThemeFlow.asStateFlow()"""

content = content.replace("""    private val _chatMessages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val chatMessages: StateFlow<List<ChatMessage>> = _chatMessages.asStateFlow()""", new_flows)

# Update init() to load values
new_init = """    fun init(appContext: Context) {
        if (isInitialized) return
        context = appContext.applicationContext
        
        _orbSizeFlow.value = getOrbSize()
        _orbThemeFlow.value = getOrbTheme()"""
content = content.replace("""    fun init(appContext: Context) {
        if (isInitialized) return
        context = appContext.applicationContext""", new_init)

# Update saveOrbSize and saveOrbTheme
new_save_size = """    fun saveOrbSize(size: Float) {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        prefs?.edit()?.putFloat("orb_size", size)?.apply()
        _orbSizeFlow.value = size
    }"""
content = re.sub(r'    fun saveOrbSize\(size: Float\) \{[\s\S]*?\}', new_save_size, content)

new_save_theme = """    fun saveOrbTheme(themeIndex: Int) {
        val prefs = context?.getSharedPreferences("mj_settings", Context.MODE_PRIVATE)
        prefs?.edit()?.putInt("orb_theme", themeIndex)?.apply()
        _orbThemeFlow.value = themeIndex
    }"""
content = re.sub(r'    fun saveOrbTheme\(themeIndex: Int\) \{[\s\S]*?\}', new_save_theme, content)

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
