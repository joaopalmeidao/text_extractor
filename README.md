# Docker

1. Faça o build imagem docker com uma nova tag: `docker build -t text-extractor:<tag> .`

2. Inice o container com a tag: `docker run -it -d -p 8000:8000 text-extractor:<tag> --name text-extractor`
