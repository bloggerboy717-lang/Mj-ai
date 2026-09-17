import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace the animated title with the logo + title in top-left
old_title_pattern = r'Text\(\n\s*text = "M\.J",\n\s*style = MaterialTheme\.typography\.displayMedium,\n\s*fontWeight = FontWeight\.Bold,\n\s*color = Color\(0xFF00BFFF\), // Sky Blue Color\n\s*modifier = Modifier\n\s*\.align\(Alignment\.TopCenter\)\n\s*\.padding\(top = 64\.dp\)\n\s*\.scale\(titleScale\)\n\s*\.alpha\(titleAlpha\)\n\s*\)'

new_title_logo = """
        Row(
            modifier = Modifier
                .align(Alignment.TopStart)
                .padding(top = 48.dp, start = 24.dp)
                .scale(titleScale)
                .alpha(titleAlpha),
            verticalAlignment = Alignment.CenterVertically
        ) {
            androidx.compose.foundation.Image(
                painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.app_logo),
                contentDescription = "App Logo",
                modifier = Modifier
                    .size(48.dp)
                    .androidx.compose.ui.draw.clip(androidx.compose.foundation.shape.CircleShape)
            )
            Spacer(modifier = Modifier.width(12.dp))
            Text(
                text = "M.J",
                style = MaterialTheme.typography.displayMedium,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF00BFFF) // Sky Blue Color
            )
        }
"""
if "Row(" not in content.split("val titleAlpha")[1]:
    content = re.sub(old_title_pattern, new_title_logo, content)

    # ensure clip and width are imported
    if "import androidx.compose.foundation.layout.width" not in content:
        content = content.replace("import androidx.compose.foundation.layout.size", "import androidx.compose.foundation.layout.size\nimport androidx.compose.foundation.layout.width\nimport androidx.compose.ui.draw.clip")

    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(content)
