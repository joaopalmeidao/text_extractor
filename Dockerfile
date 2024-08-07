FROM python:3.10.9-slim
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    ffmpeg
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./text_extractor
USER root
WORKDIR /text_extractor
EXPOSE 9052
RUN chown -R root:root /text_extractor
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]