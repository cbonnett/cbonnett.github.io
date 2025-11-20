import os

# Real Tracking ID
TRACKING_ID = "G-CF8XLEYDMP"

TRACKING_CODE = f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={TRACKING_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{TRACKING_ID}');
</script>
"""

CSS_LINK = '<link rel="stylesheet" href="/improved-styles.css" type="text/css">'

def inject_updates(directory):
    tracking_count = 0
    css_count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                modified = False
                
                # 1. Inject Tracking Code
                # Check if we need to replace the placeholder or add new
                if "G-PLACEHOLDER" in content:
                    content = content.replace("G-PLACEHOLDER", TRACKING_ID)
                    modified = True
                    print(f"Updated placeholder ID in {file}")
                elif "googletagmanager.com/gtag/js" not in content:
                    if "</head>" in content:
                        content = content.replace("</head>", f"{TRACKING_CODE}\n</head>")
                        modified = True
                        tracking_count += 1
                        print(f"Injected tracking into {file}")
                
                # 2. Inject CSS Link
                if "improved-styles.css" not in content:
                    if "</head>" in content:
                        content = content.replace("</head>", f"{CSS_LINK}\n</head>")
                        modified = True
                        css_count += 1
                        print(f"Injected CSS into {file}")

                if modified:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)

    print(f"Summary: Tracking added to {tracking_count} files. CSS added to {css_count} files.")

if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Scanning directory: {current_dir}")
    inject_updates(current_dir)
