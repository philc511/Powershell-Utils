from PIL import Image
import piexif
# REPLACE THIS WITH JHEAD
# eg (base) F:\coding\Github\powershell-utils>
# jhead -mkexif -ts2001:06:20-12:00:00 "F:\Photos\2001\2001-06\67 Fam Gp 1 09061.JPG"
path = 'temp/005_2.jpg'
exif_dict = piexif.load(path)
new_exif = exif_dict
print(new_exif)
#exif_bytes = piexif.dump(new_exif)
#piexif.insert(exif_bytes, path)