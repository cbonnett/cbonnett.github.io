import os
from bs4 import BeautifulSoup

def remove_linkedin(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                
                with open(filepath, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                
                modified = False
                
                # Find links with href containing linkedin.com
                for a in soup.find_all("a", href=True):
                    if "linkedin.com" in a['href']:
                        a.decompose() # Remove the tag
                        modified = True
                
                if modified:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(str(soup))
                    print(f"Removed LinkedIn link from {file}")
                    count += 1

    print(f"Total files processed: {count}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    remove_linkedin(current_dir)
