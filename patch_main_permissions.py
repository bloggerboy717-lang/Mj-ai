import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Find checkPermissionsAndToggle and modify it
old_permissions_func = """    private fun checkPermissionsAndToggle() {
        val permissionsToRequest = mutableListOf(Manifest.permission.RECORD_AUDIO)
        
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
            permissionsToRequest.add(Manifest.permission.CALL_PHONE)
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS) != PackageManager.PERMISSION_GRANTED) {
            permissionsToRequest.add(Manifest.permission.READ_CONTACTS)
        }
        
        // Post notifications for foreground service
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                permissionsToRequest.add(Manifest.permission.POST_NOTIFICATIONS)
            }
        }"""

new_permissions_func = """    private fun checkPermissionsAndToggle() {
        val permissionsToRequest = mutableListOf(
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.CALL_PHONE,
            Manifest.permission.READ_CONTACTS,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )
        
        val neededPermissions = permissionsToRequest.filter { 
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED 
        }.toMutableList()
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                neededPermissions.add(Manifest.permission.POST_NOTIFICATIONS)
            }
        }"""

content = content.replace(old_permissions_func, new_permissions_func)

old_check = """        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) {
            checkOverlayPermissionAndStartService()
            viewModel.toggleConnection()
        } else {
            requestPermissionLauncher.launch(permissionsToRequest.toTypedArray())
        }"""

new_check = """        if (neededPermissions.isEmpty()) {
            checkOverlayPermissionAndStartService()
            viewModel.toggleConnection()
        } else {
            requestPermissionLauncher.launch(neededPermissions.toTypedArray())
        }"""

content = content.replace(old_check, new_check)

# Let's also patch the permission result launcher
old_launcher = """    private val requestPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { permissions ->
            val audioGranted = permissions[Manifest.permission.RECORD_AUDIO] == true
            if (audioGranted) {
                checkOverlayPermissionAndStartService()
                viewModel.toggleConnection()
            }
        }"""

new_launcher = """    private val requestPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { permissions ->
            val audioGranted = permissions[Manifest.permission.RECORD_AUDIO] == true
            if (audioGranted) {
                checkOverlayPermissionAndStartService()
                viewModel.toggleConnection()
            }
        }"""

content = content.replace(old_launcher, new_launcher)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
