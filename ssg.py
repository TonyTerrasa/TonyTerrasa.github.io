from jinja2 import Environment, FileSystemLoader
from datetime import date
from os import walk

# using from https://realpython.com/primer-on-jinja-templating/#include-a-navigation-menu

SOURCE_FOLDER = 'src/'

environment = Environment(loader=FileSystemLoader(SOURCE_FOLDER))

for root, dirs, files in walk(SOURCE_FOLDER):
    for filename in files:
        # don't render files with _ at the beginning
        if filename[0] == '_':
            continue

        template = environment.get_template(filename)
        content = template.render(date=date.today())
        with open(filename, mode="w", encoding="utf-8") as message:
                message.write(content)
                print(f"... wrote {filename}")
