# ---------------------------------------------
# Script: ListAndPrintFileContents.ps1
# Description: Lists all files in the specified source directory and its subdirectories,
#              then prints the contents of each file while excluding README.MD.
#              The results are saved in the specified destination directory.
# ---------------------------------------------

# ------------------------------
# 1. Define the Folder Path for Source and Destination
# ------------------------------

# Prompt the user for the source directory (where the code files are located)
$SourceDirectory = Read-Host "Enter the source directory path (where your code is located)"

# Validate source directory path
if (-Not (Test-Path -Path $SourceDirectory)) {
    Write-Host "Error: The source directory '$SourceDirectory' does not exist." -ForegroundColor Red
    exit
}

# Prompt the user for the destination directory
$DestinationDirectory = Read-Host "Enter the destination directory path (e.g., C:\MyCodeAnalysisProject)"

# Validate destination directory path
if (-Not (Test-Path -Path $DestinationDirectory)) {
    Write-Host "Error: The destination directory '$DestinationDirectory' does not exist." -ForegroundColor Red
    exit
}

# ------------------------------
# 2. Define Allowed File Extensions (Optional)
# ------------------------------

# Specify which file types to process.
$AllowedExtensions = @("txt", "md", "csv", "log", "json", "xml", "ps1", "go", "py", "js", "css", "mod", "sql")

# ------------------------------
# 3. Retrieve All Files from Source Directory
# ------------------------------

# Get all files within the source directory and its subdirectories, excluding README.MD in the top-level directory.
try {
    $Files = Get-ChildItem -Path $SourceDirectory -Recurse -File | Where-Object {
        # Exclude README.MD from the top-level directory
        $_.FullName -notlike "$SourceDirectory\README.MD"
    }
} catch {
    Write-Host "Error retrieving files: $_" -ForegroundColor Red
    exit
}

# ------------------------------
# 4. Process Each File and Output to Destination Directory
# ------------------------------

# Define the output file in the destination directory
$OutputFile = Join-Path -Path $DestinationDirectory -ChildPath "processed_code_output.txt"

# Initialize an empty array to hold the output content
$Output = @()

foreach ($File in $Files) {
    # Check if the file has an allowed extension (if filtering is enabled)
    if ($AllowedExtensions.Count -gt 0) {
        $fileExtension = $File.Extension.TrimStart('.').ToLower()
        if (-Not ($AllowedExtensions -contains $fileExtension)) {
            Write-Host "Skipping unsupported file type: $($File.FullName)" -ForegroundColor Yellow
            continue
        }
    }

    # Add file name to output
    $Output += "----------------------------------------"
    $Output += "File: $($File.FullName)"
    $Output += "----------------------------------------"

    # Attempt to read and display the file content.
    try {
        $Content = Get-Content -Path $File.FullName -ErrorAction Stop -Raw
        $Output += $Content + "`n`n"
    } catch {
        # Append the error message to the output without ForegroundColor
        $Output += "Unable to read file: $($File.FullName). Error: $_`n`n"
    }
}

# ------------------------------
# 5. Save Output to the Destination Directory
# ------------------------------

# Save the output to the specified file in the destination directory
$Output | Out-File -FilePath $OutputFile -Encoding utf8

# ------------------------------
# 6. Completion Message
# ------------------------------

Write-Host "Completed processing all files in '$SourceDirectory'. Output saved to '$OutputFile'." -ForegroundColor Magenta
