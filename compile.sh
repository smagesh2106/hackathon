python -m compileall -b src/

# Create a directory for the compiled files
mkdir -p build/logs build/uploads/ build/backups
cp -r templates build/
cp -r src/data build/

cp .env build/
cp requirements.txt build/
cp .dockerignore build/
cp Dockerfile build/
cp docker-compose.yml build/



# Copy the compiled .pyc files maintaining the directory structure
cd src
find . -name '*.pyc' -exec sh -c '
  for file; do  
    dest="../build/${file}"
    mkdir -p "$(dirname "$dest")"
    mv "$file" "$dest"
  done
' sh {} +

# Go back to the root directory
cd ..
