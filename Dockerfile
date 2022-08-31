FROM python:alpine

ENV VIRTUAL_ENV=/opt/venv

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk add --no-cache i2c-tools libgpiod-dev gcc libc-dev linux-headers py3-pillow procps zlib-dev jpeg-dev freetype-dev\
    && pip3 install --upgrade pip adafruit-python-shell setuptools RPI.GPIO adafruit-blinka adafruit-circuitpython-ssd1306 Pillow

WORKDIR /opt/stats

COPY PixelOperator.ttf lineawesome-webfont.ttf stats2.py /opt/stats/

ENTRYPOINT [ "python", "stats.py" ]