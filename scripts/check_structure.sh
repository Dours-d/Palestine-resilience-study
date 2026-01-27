'EOF'
#!/bin/bash

echo "=== Repository Structure Check ==="
echo ""

# Check for common issues
echo "1. Checking for large files (>10MB)..."
find . -type f -size +10M ! -path "./.git/*" | head -10

echo ""
echo "2. Checking for unnecessary binary files..."
find . -type f -exec file {} \; | grep -E "(executable|binary)" | grep -v ".git" | head -10

echo ""
echo "3. Checking repository size..."
du -sh .
du -sh * | sort -hr

echo ""
echo "4. Checking for sensitive files..."
find . -name "*.env*" -o -name "*secret*" -o -name "*key*" -o -name "*password*" | grep -v ".git"

echo ""
echo "=== Structure Complete ==="
EOF

chmod +x check_structure.sh
