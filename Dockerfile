###########################################################################
# Dependency Exporter
###########################################################################

FROM python:3.8-slim-bullseye AS deps-builder

RUN apt update -y && apt upgrade -y && apt install curl -y

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN $HOME/.local/bin/poetry config virtualenvs.create false 

WORKDIR /app

COPY ./norma/pyproject.toml ./norma/
COPY ./norma/poetry.lock ./norma/

RUN cd norma && $HOME/.local/bin/poetry remove tensorflow tensorflow-macos tensorflow-metal jupyterlab

RUN cd /app/norma && $HOME/.local/bin/poetry export -f requirements.txt >> requirements.txt

###########################################################################
# Library Builder
###########################################################################

FROM python:3.8-bullseye AS lib-builder

RUN apt update -y && apt upgrade -y && apt install curl build-essential -y
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip3 install maturin

WORKDIR /app

# Dependency Build Cache
COPY ./libbaghchal/Cargo.toml ./libbaghchal/Cargo.toml ./libbaghchal/
RUN mkdir ./libbaghchal/src && touch ./libbaghchal/src/lib.rs

RUN cd /app/libbaghchal && cargo build --release

RUN rm ./libbaghchal/Cargo.toml ./libbaghchal/Cargo.lock

# Actutal Build
COPY ./libbaghchal/ /app/libbaghchal/

RUN cd /app/libbaghchal && maturin build --release --manylinux off

###########################################################################
# Prod image
###########################################################################

FROM tensorflow/tensorflow:2.11.0-gpu
WORKDIR /app

COPY --from=deps-builder /app/norma/requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY --from=lib-builder /app/libbaghchal/target/wheels/libbaghchal*.whl .
RUN python --version
RUN pip install libbaghchal*.whl
RUN rm libbaghchal*.whl

RUN rm requirements.txt

COPY ./keys/id_rsa /keys/id_rsa

RUN apt update -y && apt upgrade -y
RUN apt install autossh git openssh-server sudo -y

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 daze

RUN  echo 'daze:daze' | chpasswd


COPY ./keys/id_rsa /home/ubuntu/.ssh/
COPY ./keys/id_rsa /root/.ssh/

RUN service ssh start

EXPOSE 22

COPY ./start-script.sh /
RUN chmod +x /start-script.sh

CMD exec /start-script.sh
