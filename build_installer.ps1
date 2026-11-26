$ErrorActionPreference = "Stop"

$compilerCandidates = @(
    (Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 6\ISCC.exe"),
    (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe"),
    (Join-Path $env:ProgramFiles "Inno Setup 6\ISCC.exe")
)
$compiler = $compilerCandidates |
    Where-Object { Test-Path $_ } |
    Select-Object -First 1

if (-not $compiler) {
    throw "Inno Setup 6 was not found. Install it before building the installer."
}

Push-Location $PSScriptRoot
$workFile = [System.IO.Path]::GetTempFileName()
$workDirectory = $workFile
Remove-Item -LiteralPath $workFile
New-Item -ItemType Directory -Path $workDirectory | Out-Null
$appOutput = Join-Path $PSScriptRoot "dist\release\Hipermiklos_YTDownloader"
try {
    if (Test-Path $appOutput) {
        Remove-Item -LiteralPath $appOutput -Recurse -Force
    }

    & pyinstaller --clean --noconfirm --distpath dist\release --workpath $workDirectory Hipermiklos_YTDownloader.spec
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller failed with exit code $LASTEXITCODE."
    }

    & $compiler installer.iss
    if ($LASTEXITCODE -ne 0) {
        throw "Inno Setup failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
    if (Test-Path $workDirectory) {
        Remove-Item -LiteralPath $workDirectory -Recurse -Force
    }
}
