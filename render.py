import os
import re
import shutil

import markdown2
from jinja2 import Environment, FileSystemLoader

# clear output folder
os.system('rm -rf output/*')
# Create output directory
os.makedirs('output', exist_ok=True)
os.makedirs('output/people', exist_ok=True)
# Function to convert markdown to html
def markdown_to_html(markdown_file):
    with open(markdown_file, 'r') as file:
        content = file.readlines()
    content = [line for line in content if line.strip() != "_For instructions on how to use this template and contribute to the repository, please refer to the README file._"]
    return markdown2.markdown(''.join(content))
# Set up jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))

# Iterate through people directories
all_people = []

def extract_name(markdown_file):
    with open(markdown_file, 'r') as file:
        first_line = file.readline().strip()
        name = first_line.split(' ')[-2].strip('[]') + ' ' + first_line.split(' ')[-1].strip('[]')
        return name
    
# Read navigation snippet if it exists
nav_html = None
if os.path.exists('templates/component/nav.html'):
    with open('templates/component/nav.html', 'r') as file:
        nav_html = file.read()
    people_nav_html = re.sub(r'href="([^"]+)"', r'href="../../\1"', nav_html)

# In the loop through people's directories
for people_dir in os.listdir('docs/people'):
    if people_dir == '.DS_Store' or people_dir == 'TEMPLATE':
        continue
    base_dir = os.path.join('people', people_dir)
    os.makedirs('output/'+base_dir, exist_ok=True)
    index_md_path = os.path.join('docs/people', people_dir, 'index.md')
    name = extract_name(index_md_path)
    custom_css_path = os.path.join('docs/people', people_dir, 'custom/custom.css')
    custom_js_path = os.path.join('docs/people', people_dir, 'custom/custom.js')
    # Check if the custom files exist
    # custom_css = custom_css_path if os.path.exists(custom_css_path) else None
    # custom_js = custom_js_path if os.path.exists(custom_js_path) else None
    if os.path.exists(custom_css_path):
        custom_css_name = os.path.join(base_dir, 'custom.css')
        shutil.copy(custom_css_path, 'output/'+custom_css_name)
        custom_css = 'custom.css'
    else:
        custom_css = None
        
    if os.path.exists(custom_js_path):
        custom_js_name = os.path.join(base_dir, 'custom.js')
        shutil.copy(custom_js_path, 'output/'+custom_js_name)
        custom_js = 'custom.js'
    else:
        custom_js = None

    # copy assets folder
    assets_dir = os.path.join('docs/people', people_dir, 'assets')
    if os.path.exists(assets_dir):
        shutil.copytree(assets_dir, 'output/'+os.path.join(base_dir, 'assets'))
    else:
        assets_dir = None
    # Read markdown files
    index_html = markdown_to_html(index_md_path)
    if os.path.exists(os.path.join('docs/people', people_dir, 'projects.md')):
        projects_html = markdown_to_html(os.path.join('docs/people', people_dir, 'projects.md'))
    else:
        projects_html = None
    if os.path.exists(os.path.join('docs/people', people_dir, 'publications.md')):
        publications_html = markdown_to_html(os.path.join('docs/people', people_dir, 'publications.md'))
    else:
        publications_html = None

    # Render individual HTML template
    template = env.get_template('people_template.html')
    output = template.render(index=index_html, projects=projects_html, publications=publications_html, custom_css=custom_css, custom_js=custom_js, name=name, head_nav=people_nav_html)
    with open(os.path.join('output', base_dir, 'index.html'), 'w') as file:
        file.write(output)
        
    pin_path = os.path.join('docs/people', people_dir, 'pin.md')
    if os.path.exists(pin_path):
        pin_html = markdown_to_html(pin_path)
    else:
        pin_html = None
    all_people.append({'name': name, 'pin': pin_html, 'dir': people_dir})
        


# Render collective HTML file
template = env.get_template('all_people_template.html')
# sort all_people by first name
all_people = sorted(all_people, key=lambda x: x['name'].split(' ')[-2])
output = template.render(people=all_people, head_nav=nav_html)
with open('output/all_people.html', 'w') as file:
    file.write(output)
# copy to index.html
os.system('cp output/all_people.html output/index.html')
# copy static files
os.system('cp -r templates/static/* output/')