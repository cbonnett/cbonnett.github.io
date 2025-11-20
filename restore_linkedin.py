import os
import re

LINKEDIN_HTML = '<li><a href="https://www.linkedin.com/in/cbonnett">LinkedIn</a></li>'

def restore_linkedin(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                modified = False
                
                # Check if LinkedIn link is missing but main-navigation exists
                if "LinkedIn" not in content and '<ul class="main-navigation">' in content:
                    # Inject it at the beginning of the list
                    content = content.replace('<ul class="main-navigation">', f'<ul class="main-navigation">\n        {LINKEDIN_HTML}')
                    modified = True
                    print(f"Restored LinkedIn link in {file}")
                
                # If main-navigation is missing (unlikely given previous script, but possible), we might need to reconstruct it.
                # But my previous script only removed the LI, not the UL.
                
                if modified:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    count += 1

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Scanning directory: {current_dir}")
    restore_linkedin(current_dir)
