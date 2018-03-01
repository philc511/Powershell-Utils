gci . -recurse -filter *.MOD | foreach { 
    $newName =  $_.Name.replace("MOD", "MPG")
    write-output $_.Name
    Rename-Item -Path $_.FullName -NewName $newName
}