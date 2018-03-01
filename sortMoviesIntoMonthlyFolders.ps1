<#
.SYNOPSIS
Sorts into folders

.DESCRIPTION
Sorts files with m* extension into folders
#>
gci . -filter *.M* | foreach { 
    $folder =  $_.LastWriteTime | Get-Date -format "yyyy-MM"
    write-output $_.Name
    if (-Not(Test-Path -Path $folder)) {
        New-Item -Path $folder -ItemType Directory
    }
    Move-Item -Path $_.Name -Destination $folder 
}