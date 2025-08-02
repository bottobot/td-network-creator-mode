#!/bin/bash
# Shell script to convert Mermaid diagrams to PDF and SVG
# Requires Node.js and mermaid-cli (npm install -g @mermaid-js/mermaid-cli)

echo "Converting Mermaid diagrams to PDF and SVG..."

# Check if mmdc is installed
if ! command -v mmdc &> /dev/null; then
    echo "Error: mermaid-cli not found. Please install it with:"
    echo "npm install -g @mermaid-js/mermaid-cli"
    exit 1
fi

# Convert all .mmd files in current directory
for file in *.mmd; do
    if [ -f "$file" ]; then
        echo "Converting $file..."
        base_name="${file%.mmd}"
        
        # Convert to PDF
        if mmdc -i "$file" -o "${base_name}.pdf" -t dark -b transparent; then
            echo "  - PDF created: ${base_name}.pdf"
        else
            echo "  - Error creating PDF for $file"
        fi
        
        # Convert to SVG
        if mmdc -i "$file" -o "${base_name}.svg" -t dark -b transparent; then
            echo "  - SVG created: ${base_name}.svg"
        else
            echo "  - Error creating SVG for $file"
        fi
        
        # Convert to PNG as backup
        if mmdc -i "$file" -o "${base_name}.png" -t dark -b transparent -w 2048 -H 1536; then
            echo "  - PNG created: ${base_name}.png"
        else
            echo "  - Error creating PNG for $file"
        fi
    fi
done

echo ""
echo "Conversion complete!"