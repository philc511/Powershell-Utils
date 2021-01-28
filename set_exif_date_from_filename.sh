# For all files in the current folder,
# get the year month date from filename in format XXX-YYYYMMDD-XXXX.*
# and set the Exif date to this date
for f in *
do
	fdate=$(echo $f   | awk -F - '{print $2}')
	year=$(echo $fdate | cut -c 1-4)
	month=$(echo $fdate | cut -c 5-6)
	day=$(echo $fdate | cut -c 7-8)
        jhead -mkexif -ds$year:$month:$day $f
done
