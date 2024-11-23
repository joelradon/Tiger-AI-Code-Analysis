
#!/bin/bash
# This script lists all files in the specified source directory and its subdirectories,
# then prints the contents of each file while excluding README.md.

# 1. Define the Folder Path for Source and Destination
echo "Enter the source directory path (where your code is located):"
read SOURCE_DIR

# Validate source directory path
if [ ! -d "$SOURCE_DIR" ]; then
  echo "Error: The source directory '$SOURCE_DIR' does not exist."
  exit 1
fi

echo "Enter the destination directory path (e.g., /path/to/destination):"
read DEST_DIR

# Validate destination directory path
if [ ! -d "$DEST_DIR" ]; then
  echo "Error: The destination directory '$DEST_DIR' does not exist."
  exit 1
fi

# 2. Define Allowed File Extensions
ALLOWED_EXTENSIONS=("txt" "md" "csv" "log" "json" "xml" "go" "py" "js" "css" "mod" "sql")

# 3. Retrieve All Files from Source Directory
OUTPUT_FILE="$DEST_DIR/processed_code_output.txt"
> $OUTPUT_FILE  # Empty the output file

find "$SOURCE_DIR" -type f ! -name "README.md" | while read FILE; do
  EXT="${FILE##*.}"
  if [[ " ${ALLOWED_EXTENSIONS[@]} " =~ " $EXT " ]]; then
    echo "----------------------------------------" >> $OUTPUT_FILE
    echo "File: $FILE" >> $OUTPUT_FILE
    echo "----------------------------------------" >> $OUTPUT_FILE
    cat "$FILE" >> $OUTPUT_FILE
    echo -e "

" >> $OUTPUT_FILE
  else
    echo "Skipping unsupported file type: $FILE"
  fi
done

echo "Completed processing all files. Output saved to '$OUTPUT_FILE'."
