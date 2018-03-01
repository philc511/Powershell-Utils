gci . -filter *.MOD | foreach { 
    $newName =  $_.LastWriteTime | Get-Date -format "yyyy-MM-dd hh.mm.ss"
    write-output $_.Name
    Rename-Item -Path $_.Name -NewName ($newName+".MOD")
}