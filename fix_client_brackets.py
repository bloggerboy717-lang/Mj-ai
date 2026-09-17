import re

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'r') as f:
    content = f.read()

bad_str = """        } catch (e: Exception) {
            Log.e("GeminiLiveClient", "Error sending message", e)
        }
    } catch (e: Exception) {
            Log.e("GeminiLiveClient", "Error sending message", e)
        }
    }"""
    
good_str = """        } catch (e: Exception) {
            Log.e("GeminiLiveClient", "Error sending message", e)
        }
    }"""

content = content.replace(bad_str, good_str)

with open('app/src/main/java/com/example/gemini/GeminiLiveClient.kt', 'w') as f:
    f.write(content)
