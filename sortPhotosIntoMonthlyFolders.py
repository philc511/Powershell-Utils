from pathlib import Path
from PIL import Image, ExifTags
from shutil import copy2

def info(f):
    img = Image.open(f)
    exif_data = img._getexif()
    # return  {
    #     ExifTags.TAGS[k]: v
    #         for k, v in exif_data.items()
    #         if k in ExifTags.TAGS
    #     }
    return exif_data


def get_folder(timestamp):
    year = timestamp[:4]
    year_month = timestamp[:7].replace(':', '-')
    return [year, year_month]

# TODO alert if already present
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

#root_source = 'F:/2012'
root_source = 'temp/source'
root_target = 'temp/target'

num_copied = 0
num_not_copied = 0

# for each file in the folder
for filename in Path(root_source).glob('**/*.*'):
    # check the image info
    tags = info(filename)
    
    # report if cannot be done
    # TODO

    # get the datetimeoriginal (datetime if not present), report if neither present
    # find the year/month
    if date_time_orig_tag in tags:
        folder = get_folder(tags[date_time_orig_tag])
    elif date_time_tag in tags:
        folder = get_folder(tags[date_time_tag])
    else:
        folder = ['0000','0000-00']

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