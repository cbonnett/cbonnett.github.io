import os
from bs4 import BeautifulSoup

def fix_header_link(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                
                with open(filepath, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                
                modified = False
                
                # Find the LCARS header h1
                header = soup.find(class_="lcars-header")
                if header:
                    h1 = header.find("h1")
                    if h1:
                        # Check if it already has a link
                        if not h1.find("a"):
                            text = h1.get_text(strip=True)
                            new_a = soup.new_tag("a", href="https://cbonnett.github.io/")
                            new_a.string = text
                            h1.string = ""
                            h1.append(new_a)
                            modified = True
                
                if modified:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(str(soup))
                    print(f"Fixed header link in {file}")
                    count += 1

    print(f"Total files processed: {count}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    fix_header_link(current_dir)
