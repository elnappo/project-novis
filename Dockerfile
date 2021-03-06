FROM ubuntu:rolling

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

RUN groupadd --system app && useradd --no-log-init --system --gid app app

RUN apt-get update && apt-get dist-upgrade --assume-yes && apt-get install --assume-yes --no-install-recommends\
    bash \
    git \
    python3-minimal \
    python3-venv \
    locales \
    liblz4-1 \
    # GeoDjango requirements
    binutils \
    libproj-dev \
    gdal-bin \
 && rm -rf /var/lib/apt/lists/* \
 && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

COPY requirements.txt /requirements.txt
RUN apt-get update && apt-get install --assume-yes --no-install-recommends build-essential python3-dev libpq-dev gcc liblz4-dev\
 && python3 -m venv /venv \
 && /venv/bin/pip install --upgrade pip \
 && /venv/bin/pip install --upgrade --no-cache-dir --requirement /requirements.txt \
 && apt-get purge --assume-yes build-essential python3-dev libpq-dev gcc liblz4-dev\
 && apt-get autoremove --assume-yes \
 && rm -rf /var/lib/apt/lists/*

COPY . /code/
WORKDIR /code/

RUN DJANGO_DEBUG=true python manage.py collectstatic --noinput

USER app
EXPOSE 8000

ENTRYPOINT ["/code/docker-entrypoint.sh"]
