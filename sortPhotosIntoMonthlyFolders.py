from pathlib import Path
from PIL import Image, ExifTags
from shutil import copy2
from datetime import datetime
import re
import os

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
    target_filename = target / filename.name
    marker = 1
    while (target_filename).exists():
        source_size = os.path.getsize(filename)
        target_size = os.path.getsize(target_filename)
        if (source_size == target_size):
            return 1
        else:
            target_filename = target / (target_filename.stem + '-(' + str(marker) +')' + target_filename.suffix)
            marker += 1
    copy2(filename, target_filename)
    return 0

def find_earliest_date_time_val(date_time_tags, valid_tag_pattern, tags):
    if tags is None:
        return None
    
    date_times = []
    for t in date_time_tags:
        if t in tags and p.match(tags[t]):
            date_times.append(tags[t])
        
    if len(date_times) > 0:
        return sorted(date_times)[0]

    return None

date_time_tags = []
# find datetimeoriginal tag
for k, v in ExifTags.TAGS.items():
    if v == 'DateTimeOriginal':
        date_time_orig_tag = k
        date_time_tags.append(k)
    if v == 'DateTime':
        date_time_tag = k
        date_time_tags.append(k)

    if v == 'DateTimeDigitized':
        date_time_digitized_tag = k
        date_time_tags.append(k)


#root_source = 'F:/Cloudstation/Pictures/2005'
root_source = 'temp/source'
root_target = 'temp/target'
#root_target = 'F:/Photos'

# Regexp to check that EXIF dates are valid
p = re.compile('\d\d\d\d:\d\d.*')

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

    ###
    debug = False
    if debug:
        print(filename)
    ###

    first_date_time = find_earliest_date_time_val(date_time_tags, p, tags)

    if first_date_time is None:
        folder = get_folder(file_mod_date, 'x')
        num_no_exif += 1        
    else:
        folder = get_folder(first_date_time, '')

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