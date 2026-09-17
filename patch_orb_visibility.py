import re

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'r') as f:
    content = f.read()

# Add isOrbVisible flow
old_vars = """    private val _orbThemeFlow = MutableStateFlow(0)
    val orbThemeFlow: StateFlow<Int> = _orbThemeFlow.asStateFlow()"""

new_vars = """    private val _orbThemeFlow = MutableStateFlow(0)
    val orbThemeFlow: StateFlow<Int> = _orbThemeFlow.asStateFlow()
    
    private val _isOrbVisible = MutableStateFlow(true)
    val isOrbVisible: StateFlow<Boolean> = _isOrbVisible.asStateFlow()
    
    fun setOrbVisible(visible: Boolean) {
        _isOrbVisible.value = visible
    }"""

if "val isOrbVisible" not in content:
    content = content.replace(old_vars, new_vars)

# Reset orb visibility when connecting
old_toggle = """    fun toggleConnection() {
        when (_state.value) {
            AssistantState.IDLE, AssistantState.ERROR -> {
                isUserRequestedDisconnect = false"""

new_toggle = """    fun toggleConnection() {
        when (_state.value) {
            AssistantState.IDLE, AssistantState.ERROR -> {
                isUserRequestedDisconnect = false
                _isOrbVisible.value = true"""

content = content.replace(old_toggle, new_toggle)

with open('app/src/main/java/com/example/core/AssistantCore.kt', 'w') as f:
    f.write(content)
