$outputExtension = ".MP4"
$bitrate = 160
$channels = 2

gci . -filter *.mov | Rename-Item -NewName { $_.Name -replace '_(\d\d)-(\d\d)-(\d\d)',' $1.$2.$3' }

foreach($inputFile in get-childitem -recurse -Filter *.mov)
{ 
  $outputFileName = [System.IO.Path]::GetFileNameWithoutExtension($inputFile.FullName) + $outputExtension;
  $outputFileName = [System.IO.Path]::Combine($inputFile.DirectoryName, $outputFileName);
 
  $programFiles = ${env:ProgramFiles(x86)};
  if($programFiles -eq $null) { $programFiles = $env:ProgramFiles; }
 
  $processName = $programFiles + "\VideoLAN\VLC\vlc.exe"
  $processArgs = "-I dummy -vvv `"$($inputFile.FullName)`" --sout-avcodec-strict=-2 --sout=#transcode{vcodec=h264,acodec=mp4a,samplerate=44100}:standard{access=file,mux=mp4,dst=`"$outputFileName`"} vlc://quit"
 
  start-process $processName $processArgs -wait
  
  $timestamp = $inputFile.LastWriteTime;
  $timestampString = $timestamp | Get-Date -format "yyyy-MM-dd HH:mm:ssT.000000Z";
  $exifProcessName = "C:\apps\exiftool\exiftool.exe"
  &$exifProcessName -CreateDate="$timestampString" $outputFileName -overwrite_original
  Set-ItemProperty -Path $outputFileName -Name LastWriteTimeUTC -Value $timestamp
  Set-ItemProperty -Path $outputFileName -Name CreationTimeUTC -Value $timestamp
}
  
