# --- CONFIGURATION ---
$ErrorActionPreference = "Stop"

$OutFiles = @(
    "full_project_context.md"
)

$IgnoredExtensions = @(
    ".db",
    ".sqlite",
    ".sqlite3",
    ".db3",
    ".png",
    ".exe",
    ".jpg",
    ".pdf",
    ".pyz",
    ".zip",
    ".pkg",
    ".pickle",
    ".doctree"
)

try {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw "The 'git' command was not found. Make sure it is installed and in your PATH."
    }
    $isGitRepo = git rev-parse --is-inside-work-tree --quiet 2>$null
    if ($isGitRepo -ne "true") {
        throw "Not inside a Git repository."
    }
} catch {
    Write-Host "Error: 'git' is not working or you are not inside a Git repository." -ForegroundColor Red
    exit 1
}

Write-Host "Starting project concatenation process..." -ForegroundColor Green

$contentBuilder = [System.Text.StringBuilder]::new()

$null = $contentBuilder.AppendLine("## 1. PROJECT METADATA ##")
$null = $contentBuilder.AppendLine("Generation date: $(Get-Date)")
$null = $contentBuilder.AppendLine("Project directory: $((Get-Location).Path)")
$null = $contentBuilder.AppendLine("Current commit: $(git rev-parse --short HEAD)")
$null = $contentBuilder.AppendLine() 
$null = $contentBuilder.AppendLine("## 2. FULL FILE STRUCTURE ##")

$allFiles = git ls-files -c --others --exclude-standard

if (Get-Command tree -ErrorAction SilentlyContinue) {
    $null = $contentBuilder.AppendLine("(Displaying the full directory tree, as Windows 'tree' lacks --fromfile)")
    $treeOutput = tree /F /A | Out-String
    $null = $contentBuilder.Append($treeOutput)
} else {
    foreach ($line in $allFiles) {
        $null = $contentBuilder.AppendLine($line)
    }
}
$null = $contentBuilder.AppendLine()
$null = $contentBuilder.AppendLine("## 3. CONTENT OF ALL FILES ##")

foreach ($file in $allFiles) {
    if ($OutFiles -contains $file) { continue }
    if ($MyInvocation.MyCommand.Name -eq $file) { continue }

    $fileExtension = [System.IO.Path]::GetExtension($file).ToLower()
    if ($IgnoredExtensions -contains $fileExtension) {
        Write-Host "  -> Ignoring binary/excluded file: $file" -ForegroundColor Yellow
        continue 
    }

    if (Test-Path $file -PathType Leaf) {
        Write-Host "  -> Processing: $file"
        $fileText = Get-Content $file -Raw -ErrorAction SilentlyContinue

        $null = $contentBuilder.AppendLine("--- START OF FILE: $file ---")
        $null = $contentBuilder.AppendLine($fileText)
        $null = $contentBuilder.AppendLine("--- END OF FILE: $file ---")
        $null = $contentBuilder.AppendLine()
    }
}

$finalContent = $contentBuilder.ToString()

foreach ($outFile in $OutFiles) {
    Write-Host "  -> Writing to output file: $outFile" -ForegroundColor Cyan
    Set-Content -Path $outFile -Value $finalContent -Encoding UTF8
}

Write-Host "-------------------------------------------------"
Write-Host "Process completed." -ForegroundColor Green