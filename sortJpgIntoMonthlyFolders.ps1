<#
.SYNOPSIS
Sorts into folders

.DESCRIPTION
Sorts files with m* extension into folders
#>
#. ".\Get-Images.ps1"
#Get-Images -Source C:\Users\philc\OneDrive\Pictures\whatsapp -Extension .jpg -Verbose
$objShell  = New-Object -ComObject Shell.Application
$cwd = Get-Location
$objFolder = $objShell.namespace($cwd.Path)
Write-Output $objFolder
Write-Output $objFolder.getDetailsOf($objFolder.items(),12)
Write-Output $objFolder.getDetailsOf($objFolder.items(),4)
foreach ($File in $objFolder.items()) { 
    Write-Output "Checking file '$($File.Path)'"
    if ($objFolder.getDetailsOf($File, 2) -eq "JPG File") {
        Write-Output "Processing file '$($File.Path)'"
        $a = $objFolder.getDetailsOf($File,12)
        if ($a.length -gt 0) {
            $folder =  "F:\Photos\" + $a.substring(9,4) + "\" + $a.substring(9,4) + "-" +$a.substring(5,2)
        } else {
            $a = $objFolder.getDetailsOf($File,3)
            Write-Output "DATE CREATED =  '$($a)'"
            $folder =  "F:\Photos\" + $a.substring(6,4) + "\" + $a.substring(6,4) + "-" +$a.substring(3,2) + "x"
        }
        if (-Not(Test-Path -Path $folder)) {
            New-Item -Path $folder -ItemType Directory
        }
        Move-Item -Path $File.Path -Destination $folder 
    }
}

# gci "F:\AAAPhotosToBeReviewedOct18\Other" -recurse -directory | foreach { 
# #     $folder =  $_.LastWriteTime | Get-Date -format "yyyy-MM"
#     write-output $_.fullName
#     $objFolder = $objShell.namespace($_.fullName)
#     foreach ($File in $objFolder.items()) { 
#         if ($objFolder.getDetailsOf($File, 156) -in $Extension) {
#             Write-Output "Processing file '$($File.Path)'"
#         }
#     }
# #     if (-Not(Test-Path -Path $folder)) {
# #         New-Item -Path $folder -ItemType Directory
# #     }
# #     Move-Item -Path $_.Name -Destination $folder 
# }