import os
import markdown2
import shutil
from jinja2 import Environment, FileSystemLoader

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

# Define the directory for custom CSS files in the output
custom_output_dir = 'customs'
os.makedirs(custom_output_dir, exist_ok=True)

# In the loop through people's directories
for person_dir in os.listdir('docs/people'):
    index_md_path = os.path.join('docs/people', person_dir, 'index.md')
    name = extract_name(index_md_path)
    custom_css_path = os.path.join('docs/people', person_dir, 'custom/custom.css')
    custom_js_path = os.path.join('docs/people', person_dir, 'custom/custom.js')
    # Check if the custom files exist
    # custom_css = custom_css_path if os.path.exists(custom_css_path) else None
    # custom_js = custom_js_path if os.path.exists(custom_js_path) else None
    if os.path.exists(custom_css_path):
        custom_css = os.path.join(custom_output_dir, f'{person_dir}.css')
        shutil.copy(custom_css_path, 'output/'+custom_css)
    else:
        custom_css = None
        
    if os.path.exists(custom_js_path):
        custom_js = os.path.join(custom_output_dir, f'{person_dir}.js')
        shutil.copy(custom_js_path, 'output/'+custom_js)
    else:
        custom_js = None

    # Rest of the code remains the same, except you'll add the name to the all_people list
    all_people.append({'dir': person_dir, 'name': name})
    # Read markdown files
    index_html = markdown_to_html(index_md_path)
    projects_html = markdown_to_html(os.path.join('docs/people', person_dir, 'projects.md'))
    publications_html = markdown_to_html(os.path.join('docs/people', person_dir, 'publications.md'))

    # Render individual HTML template
    template = env.get_template('person_template.html')
    output = template.render(index=index_html, projects=projects_html, publications=publications_html, custom_css=custom_css, custom_js=custom_js)
    with open(os.path.join('output', f'{person_dir}.html'), 'w') as file:
        file.write(output)


# Render collective HTML file
template = env.get_template('all_people_template.html')
output = template.render(people=all_people)
with open('output/all_people.html', 'w') as file:
    file.write(output)
# copy to index.html
os.system('cp output/all_people.html output/index.html')
# copy css file to output
os.system('cp templates/style.css output/style.css')