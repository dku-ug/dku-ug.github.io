import os
import markdown2
import shutil
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

# In the loop through people's directories
for person_dir in os.listdir('docs/people'):
    if person_dir == '.DS_Store' or person_dir == 'TEMPLATE':
        continue
    base_dir = os.path.join('people', person_dir)
    os.makedirs('output/'+base_dir, exist_ok=True)
    index_md_path = os.path.join('docs/people', person_dir, 'index.md')
    name = extract_name(index_md_path)
    custom_css_path = os.path.join('docs/people', person_dir, 'custom/custom.css')
    custom_js_path = os.path.join('docs/people', person_dir, 'custom/custom.js')
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
    assets_dir = os.path.join('docs/people', person_dir, 'assets')
    if os.path.exists(assets_dir):
        shutil.copytree(assets_dir, 'output/'+os.path.join(base_dir, 'assets'))
    else:
        assets_dir = None
    # Read markdown files
    index_html = markdown_to_html(index_md_path)
    projects_html = markdown_to_html(os.path.join('docs/people', person_dir, 'projects.md'))
    publications_html = markdown_to_html(os.path.join('docs/people', person_dir, 'publications.md'))

    # Render individual HTML template
    template = env.get_template('person_template.html')
    output = template.render(index=index_html, projects=projects_html, publications=publications_html, custom_css=custom_css, custom_js=custom_js, name=name)
    with open(os.path.join('output', base_dir, 'index.html'), 'w') as file:
        file.write(output)
        
    pin_path = os.path.join('docs/people', person_dir, 'pin.md')
    if os.path.exists(pin_path):
        pin_html = markdown_to_html(pin_path)
    else:
        pin_html = None
    all_people.append({'name': name, 'pin': pin_html, 'dir': person_dir})
        


# Render collective HTML file
template = env.get_template('all_people_template.html')
# sort all_people by last name
all_people = sorted(all_people, key=lambda x: x['name'].split(' ')[-1])
output = template.render(people=all_people)
with open('output/all_people.html', 'w') as file:
    file.write(output)
# copy to index.html
os.system('cp output/all_people.html output/index.html')
# copy css file to output
os.system('cp templates/style.css output/style.css')