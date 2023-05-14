# index PDF Generator

This script generates a an index from a pdf 

## Build Docker Image

To build the Docker image, navigate to the directory containing the Dockerfile and run the following command:

```bash
docker build -t index-generator .
```

## Run Docker Container

```bash
docker run -it --rm -v "$PWD":/app/content index-generator --input /app/your-input-file.pdf --whitelist /app/your-whitelist.txt--dir content/
```

## Move runscript to bin

```sh
chmod +x runContainer.sh
```

```sh
sudo ln -sf $(pwd)/runContainer.sh /usr/local/bin/pdftoindex
```