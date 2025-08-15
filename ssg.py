from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import date
import os
import sys


# using from https://realpython.com/primer-on-jinja-templating/#include-a-navigation-menu
SOURCE_FOLDER = "src/"

environment = Environment(loader=FileSystemLoader(SOURCE_FOLDER))

# base function from https://stackoverflow.com/questions/8199966/python-title-with-apostrophes
def titlize(s: str) -> str:
    words = []
    for i, w in enumerate(s.split(' ')): 
        if i == 1 or len(w) > 2:
            words.append(w.capitalize())
        else:
            words.append(w)
    return ' '.join(words)

def get_caption_from_filename(stem: str) -> str:
    """
    Turn to title case and get rid of 
    """
    caption = stem.replace('_', ' ').replace('-', ' ')
    # convert 01_filename to 1) filename
    if caption[:2].isnumeric():
        caption = str(int(caption[:2])) + ")" + caption[2:]
    return titlize(caption)



def get_media_from_folder(folder_path, base_url=""):
    """
    Get all images from a folder and return list with metadata
    """
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']
    video_extensions = ['*.mp4', '*.mov', '*.avi', '*.webm', '*.mkv']
    media_files = []


    folder = Path(folder_path)
    if not folder.exists():
        print(f"Folder {folder} not found")
        return media_files
  
    for ext in image_extensions:
        for file_path in folder.glob(ext):
            caption = get_caption_from_filename(file_path.stem)
            
            media_files.append({
                'path': f"{base_url}{file_path.relative_to('.')}",
                'alt': caption,
                'caption': caption,
                'filename': file_path.name,
                'type' : 'image',
            })


    # Get videos
    for ext in video_extensions:
        for file_path in folder.glob(ext):
            caption = get_caption_from_filename(file_path.stem)
            
            media_files.append({
                'path': f"{base_url}{file_path.relative_to('.')}",
                'alt': caption,
                'caption': caption,
                'filename': file_path.name,
                'type': 'video'
            })
    
    # Sort by filename for consistent ordering
    media_files.sort(key=lambda x: x['filename'])
    return media_files


# Global cache for carousels
carousels = {}
def get_carousels():
    global carousels
    if len(carousels) > 0:
        return carousels
    else:
        media_directory = "media/summer2025/"

        # Check if directory exists
        if not os.path.exists(media_directory):
            print(f"Media directory {media_directory} not found")
            return {}
        
        carousel_filepaths = os.listdir(media_directory)
        carousel_filepaths.sort()

        carousel_names = [s.split("-", 1)[-1] for s in carousel_filepaths if os.path.isdir(os.path.join(media_directory, s))]
        carousel_paths = [p for p in carousel_filepaths if os.path.isdir(os.path.join(media_directory, p))]

        # carousel_names = [s.split("-")[-1] for s in carousel_filepaths]
        
        # Load media for each carousel
        print("Loading carousels...")
        for name, path in zip(carousel_names, carousel_paths):
            full_path = os.path.join(media_directory, path)
            media = get_media_from_folder(full_path)
            carousels[name] = media
            print(f"  - {name}: {len(media)} files")

        # carousels = dict(zip(carousel_names, [get_media_from_folder(media_directory + p) for p in carousel_filepaths]))

        return carousels


def render(filename: str):

    template = environment.get_template(filename)
    if "summer2025" in filename:
        
        carousels = get_carousels()
        

        c01_stanford = get_media_from_folder('media/summer2025/01carousel-stanford')
        c02_graysonvisit = get_media_from_folder('media/summer2025/02carousel-graysonvisit')
        c03_diving = get_media_from_folder('media/summer2025/03carousel-diving')
        c04_arrivinginsydney  = get_media_from_folder('media/summer2025/04carousel-arrivinginsydney')
        c05_boattour  = get_media_from_folder('media/summer2025/05carousel-boattour')
        c06_whitehavenanddiving  = get_media_from_folder('media/summer2025/06carousel-whitehavenanddiving')
        content = template.render(
            date=date.today(),
            c01_stanford = c01_stanford,
            c02_graysonvisit = c02_graysonvisit,
            c03_diving = c03_diving,
            c04_arrivinginsydney = c04_arrivinginsydney,
            c05_boattour = c05_boattour,
            c06_whitehavenanddiving = c06_whitehavenanddiving,
            **carousels,
        )
    else:
        content = template.render(
            date=date.today(),
        )
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

    for root, dirs, files in os.walk(SOURCE_FOLDER):
        for filename in files:
            # don't render files with _ at the beginning
            if filename[0] == "_":
                continue

            # don't render css files
            if filename[-3:] == "css":
                continue

            if render_files == "all" or filename in render_files:
                render(filename)
