gci . -filter *.mp4 | foreach { 
    write-output $_.Name
    $folder = $_.Name.Substring(0,7)
    if (-Not(Test-Path -Path $folder)) {
        New-Item -Path $folder -ItemType Directory
    }
    Move-Item -Path $_.Name -Destination $folder 
}