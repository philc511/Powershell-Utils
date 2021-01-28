$outputExtension = ".mp4"
$bitrate = 160
$channels = 2

gci . -filter *.avi | Rename-Item -NewName { $_.Name -replace '_(\d\d)-(\d\d)-(\d\d)',' $1.$2.$3' }

foreach($inputFile in get-childitem -recurse -Filter *.avi)
{ 
  $outputFileName = [System.IO.Path]::GetFileNameWithoutExtension($inputFile.FullName) + $outputExtension;
  $outputFileName = [System.IO.Path]::Combine($inputFile.DirectoryName, $outputFileName);
 
  $programFiles = ${env:ProgramFiles(x86)};
  if($programFiles -eq $null) { $programFiles = $env:ProgramFiles; }
 
  $processName = $programFiles + "\VideoLAN\VLC\vlc.exe"
  $processArgs = "-I dummy -vvv `"$($inputFile.FullName)`" --sout-avcodec-strict=-2 --sout=#transcode{vcodec=h264,acodec=mp4a,samplerate=44100}:standard{access=file,mux=mp4,dst=`"$outputFileName`"} vlc://quit"
 
  start-process $processName $processArgs -wait
}
  
foreach($inputFile in get-childitem -recurse -Filter *.mp4)
{ 
  $timestamp = [System.IO.Path]::GetFileNameWithoutExtension($inputFile.FullName)
  $timestamp = $timestamp.replace(".", ":")
  $timestamp = $timestamp.replace(" ", "T") + ".0000000Z"
  #"2003-11-09T12:00:00.0000000Z"
  $exifProcessName = "C:\apps\exiftool\exiftool.exe"
  &$exifProcessName -CreateDate="$timestamp" $inputFile -overwrite_original
  Set-ItemProperty -Path $inputFile.FullName -Name LastWriteTimeUTC -Value $timestamp
  Set-ItemProperty -Path $inputFile.FullName -Name CreationTimeUTC -Value $timestamp
}