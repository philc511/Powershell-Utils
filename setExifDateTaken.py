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


root_source = 'F:/Photos/2005/2005-07'
#root_source = 'temp/source'
root_target = 'F:/Photos/2005/2005-07'
#root_target = 'temp/target'

# Regexp to check that EXIF dates are valid
p = re.compile('\d\d\d\d:\d\d.*')

num_copied = 0
num_not_copied = 0
num_no_exif = 0
print(1)
# for each file in the folder
for filename in Path(root_source).glob('**/*.*'):

    file_mod_date = datetime.fromtimestamp(filename.stat().st_mtime).isoformat()
    # check the image info
    try:
        tags = info(filename)
    except:
        tags = None


    first_date_time = find_earliest_date_time_val(date_time_tags, p, tags)

    print(filename)
    print(first_date_time)