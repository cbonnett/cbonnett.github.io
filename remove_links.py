import os
import re

def remove_links(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                modified = False
                
                # Remove Atom subscription block
                # <ul class="subscription" data-subscription="rss">
                #   <li><a href="..." rel="subscribe-atom">Atom</a></li>
                # </ul>
                atom_pattern = re.compile(r'<ul class="subscription".*?>.*?</ul>', re.DOTALL)
                if atom_pattern.search(content):
                    content = atom_pattern.sub('', content)
                    modified = True
                    print(f"Removed Atom link from {file}")

                # Remove LinkedIn link
                # <li><a href="https://www.linkedin.com/in/cbonnett">LinkedIn</a></li>
                linkedin_pattern = re.compile(r'<li><a href="https://www.linkedin.com/in/cbonnett">LinkedIn</a></li>')
                if linkedin_pattern.search(content):
                    content = linkedin_pattern.sub('', content)
                    modified = True
                    print(f"Removed LinkedIn link from {file}")

                # Clean up empty main-navigation if needed (optional, but good practice)
                # If the ul becomes empty or just has the empty category link
                
                if modified:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    count += 1

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Scanning directory: {current_dir}")
    remove_links(current_dir)
