FROM python:3.6

EXPOSE 5000
WORKDIR /code

RUN apt-get update && apt-get install -y \
    zlib1g-dev \
    libjpeg-dev \
    python3-pythonmagick \
    inkscape \
    xvfb \
    poppler-utils \
    libfile-mimeinfo-perl \
    qpdf \
    libimage-exiftool-perl \
    ufraw-batch \
    ffmpeg \
    imagemagick \
    scribus \
    libreoffice

ADD requirements.txt /code/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ADD . /code/

RUN chmod +x wait-for-it.sh

CMD ["sh", "-c", "./wait-for-it.sh mysql:3306 -t 0 -- flask db upgrade heads && flask run --host=0.0.0.0 --port=5000"]


