from jinja2 import Environment, FileSystemLoader
from datetime import date
from os import walk
import sys


# using from https://realpython.com/primer-on-jinja-templating/#include-a-navigation-menu
SOURCE_FOLDER = "src/"

environment = Environment(loader=FileSystemLoader(SOURCE_FOLDER))


def render(filename: str):
    template = environment.get_template(filename)
    content = template.render(date=date.today())
    with open(filename, mode="w", encoding="utf-8") as outfile:
        outfile.write(content)
        print(f"... wrote {filename}")


if __name__ == "__main__":

    # arguments determine what files to render
    if len(sys.argv) == 1 or sys.argv[1] == "-a":
        # render everything if -a or nothing given
        render_files = "all"
    else:
        # otherwise render only the given files
        render_files = sys.argv[1:]

    for root, dirs, files in walk(SOURCE_FOLDER):
        for filename in files:
            # don't render files with _ at the beginning
            if filename[0] == "_":
                continue

            if render_files == "all" or filename in render_files:
                render(filename)
