from pathlib import Path
from PIL import Image, ExifTags
from shutil import copy2
from datetime import datetime

def info(f):
    img = Image.open(f)
    exif_data = img._getexif()
    # return  {
    #     ExifTags.TAGS[k]: v
    #         for k, v in exif_data.items()
    #         if k in ExifTags.TAGS
    #     }
    return exif_data


def get_folder(timestamp, suffix):
    year = timestamp[:4]
    year_month = timestamp[:7].replace(':', '-')
    return [year, year_month + suffix]

def copy(filename, root_target, folder):
    target = Path(root_target) / folder[0]
    target.mkdir(exist_ok=True)
    target = target / folder[1]
    target.mkdir(exist_ok=True)

    if (target / filename.name).exists():
        return 1
    copy2(filename, target)
    return 0


# find datetimeoriginal tag
for k, v in ExifTags.TAGS.items():
    if v == 'DateTimeOriginal':
        date_time_orig_tag = k
    if v == 'DateTime':
        date_time_tag = k

root_source = 'F:/Cloudstation/Pictures/2004'
#root_source = 'temp/source'
#root_target = 'F:/Photos'
root_target = 'temp/target'

num_copied = 0
num_not_copied = 0
num_no_exif = 0

# for each file in the folder
for filename in Path(root_source).glob('**/*.*'):
    file_mod_date = datetime.fromtimestamp(filename.stat().st_mtime).isoformat()
    # check the image info
    try:
        tags = info(filename)
    except:
        tags = None

    if tags is None:
        folder = get_folder(file_mod_date, 'x')
        num_no_exif += 1        
    elif date_time_orig_tag in tags:
        folder = get_folder(tags[date_time_orig_tag], '')
    elif date_time_tag in tags:
        folder = get_folder(tags[date_time_tag], '')
    else:
        folder = get_folder(file_mod_date, 'x')

    # create the folder if not present
    # copy the file
    if copy(filename, root_target, folder) > 0:
        print('DID NOT COPY ' + filename.name + ' to ' + folder[1])
        num_not_copied += 1
    else:
        print('copied ' + filename.name + ' to ' + folder[1])
        num_copied += 1

print('Total photos copied: ', num_copied)
print('Total photos NOT copied: ', num_not_copied)