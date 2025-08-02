@echo off
REM Batch script to convert Mermaid diagrams to PDF and SVG
REM Requires Node.js and mermaid-cli (npm install -g @mermaid-js/mermaid-cli)

echo Converting Mermaid diagrams to PDF and SVG...

REM Check if mmdc is installed
where mmdc >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: mermaid-cli not found. Please install it with:
    echo npm install -g @mermaid-js/mermaid-cli
    exit /b 1
)

REM Convert all .mmd files in current directory
for %%f in (*.mmd) do (
    echo Converting %%f...
    
    REM Convert to PDF
    mmdc -i "%%f" -o "%%~nf.pdf" -t dark -b transparent
    if %errorlevel% equ 0 (
        echo   - PDF created: %%~nf.pdf
    ) else (
        echo   - Error creating PDF for %%f
    )
    
    REM Convert to SVG
    mmdc -i "%%f" -o "%%~nf.svg" -t dark -b transparent
    if %errorlevel% equ 0 (
        echo   - SVG created: %%~nf.svg
    ) else (
        echo   - Error creating SVG for %%f
    )
    
    REM Convert to PNG as backup
    mmdc -i "%%f" -o "%%~nf.png" -t dark -b transparent -w 2048 -H 1536
    if %errorlevel% equ 0 (
        echo   - PNG created: %%~nf.png
    ) else (
        echo   - Error creating PNG for %%f
    )
)

echo.
echo Conversion complete!
pause