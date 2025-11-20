import os

BASE_URL = "https://cbonnett.github.io"

def improve_seo(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                modified = False
                
                # 1. Upgrade HTTP to HTTPS
                if "http://cbonnett.github.io" in content:
                    content = content.replace("http://cbonnett.github.io", "https://cbonnett.github.io")
                    modified = True
                    print(f"Upgraded HTTPS in {file}")
                
                # 2. Add Canonical Tag
                if "<link rel=\"canonical\"" not in content:
                    # Construct canonical URL
                    if file == "index.html":
                        canonical_url = BASE_URL + "/"
                    else:
                        canonical_url = f"{BASE_URL}/{file}"
                    
                    canonical_tag = f"<link rel=\"canonical\" href=\"{canonical_url}\">"
                    
                    if "</head>" in content:
                        content = content.replace("</head>", f"  {canonical_tag}\n</head>")
                        modified = True
                        print(f"Added canonical tag to {file}")

                if modified:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    count += 1

    print(f"Total files improved: {count}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Scanning directory: {current_dir}")
    improve_seo(current_dir)
