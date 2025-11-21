import os
import shutil
from bs4 import BeautifulSoup

def apply_lcars_theme(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                
                # Skip if already a backup or specific files I might want to ignore?
                # For now, process all htmls.
                
                print(f"Processing {file}...")
                
                # Create backup
                shutil.copy2(filepath, filepath + ".bak")
                
                with open(filepath, "r", encoding="utf-8") as f:
                    soup = BeautifulSoup(f, "html.parser")
                
                # Check if already converted
                if soup.find(class_="lcars-container"):
                    print(f"Skipping {file}, already converted.")
                    continue
                
                # Extract Content
                
                # 1. Title
                site_title = "Adventures in Machine Learning" # Default
                header = soup.find("header", role="banner")
                if header and header.find("h1"):
                    site_title = header.find("h1").get_text(strip=True)
                
                # 2. Navigation
                nav_links = []
                nav = soup.find("nav", role="navigation")
                if nav:
                    for a in nav.find_all("a"):
                        if a.get_text(strip=True): # Skip empty links
                            nav_links.append(a)
                
                # 3. Main Content
                main_content = soup.find("div", id="main")
                if not main_content:
                    main_content = soup.find("div", id="content")
                
                if not main_content:
                    # Fallback: try to find body content if no main/content div
                    # This is risky, but let's assume the structure is consistent for now.
                    print(f"Warning: No main content found in {file}")
                    continue

                # Create New Structure
                new_body = soup.new_tag("body")
                
                container = soup.new_tag("div", attrs={"class": "lcars-container"})
                new_body.append(container)
                
                # Sidebar
                sidebar = soup.new_tag("div", attrs={"class": "lcars-sidebar"})
                container.append(sidebar)
                
                elbow = soup.new_tag("div", attrs={"class": "lcars-elbow"})
                sidebar.append(elbow)
                
                sidebar_content = soup.new_tag("div", attrs={"class": "lcars-sidebar-content"})
                sidebar.append(sidebar_content)
                
                # Add Nav Links to Sidebar
                for link in nav_links:
                    link['class'] = link.get('class', []) + ['lcars-nav-item']
                    sidebar_content.append(link)
                
                # Header
                lcars_header = soup.new_tag("div", attrs={"class": "lcars-header"})
                container.append(lcars_header)
                
                h1 = soup.new_tag("h1")
                h1.string = site_title
                lcars_header.append(h1)
                
                # Main Content Area
                lcars_main = soup.new_tag("div", attrs={"class": "lcars-main"})
                container.append(lcars_main)
                
                # Move children of old main_content to lcars_main
                # We need to copy/move them.
                # extracting them removes them from the tree, which is fine since we are building a new body.
                if main_content:
                    # We can just append the main_content div itself or its children.
                    # Let's append the children to avoid nesting divs too deep if possible, 
                    # but keeping the wrapper might preserve some existing styles if needed.
                    # However, we want to break out of the old layout.
                    # Let's append the children.
                    for child in list(main_content.contents):
                        lcars_main.append(child)

                # Replace Body
                if soup.body:
                    soup.body.replace_with(new_body)
                else:
                    soup.append(new_body)
                
                # Add CSS
                head = soup.head
                if not head:
                    head = soup.new_tag("head")
                    soup.insert(0, head)
                
                link_tag = soup.new_tag("link", rel="stylesheet", href="/theme/css/lcars.css")
                head.append(link_tag)
                
                # Save
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(str(soup))
                
                count += 1

    print(f"Total files converted: {count}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    apply_lcars_theme(current_dir)
