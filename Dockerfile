FROM python:alpine

ENV VIRTUAL_ENV=/opt/venv

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk add --no-cache i2c-tools libgpiod-dev gcc libc-dev linux-headers py3-pillow procps zlib-dev jpeg-dev freetype-dev\
    && pip3 install --upgrade pip adafruit-python-shell setuptools RPI.GPIO adafruit-blinka adafruit-circuitpython-ssd1306 Pillow

WORKDIR /opt/stats

COPY . .

COPY PixelOperator.ttf lineawesome-webfont.ttf stats.py /opt/stats/

ENTRYPOINT [ "python", "stats.py" ]

# Build: docker build . -t test-stats
# Use: docker run --network=host --device=/dev/i2c-1 --device=/dev/gpiomem -d --name test test-stats
# Debug: docker run --entrypoint=/bin/sh -it --network=host --device=/dev/i2c-1 --device=/dev/gpiomem -d --name test test-stats