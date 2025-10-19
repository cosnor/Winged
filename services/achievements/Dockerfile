# Dockerfile.lfs
FROM python:3.11.8-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /code

# instalar herramientas necesarias y git-lfs (via packagecloud script)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl git gnupg2 && \
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt-get update && apt-get install -y --no-install-recommends git-lfs && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# argumentos para el repo y branch (modifica si tu ruta es distinta)
ARG REPO_URL=https://github.com/cosnor/Winged.git
ARG REPO_BRANCH=dev

# clonar sólo la rama y traer LFS (si repo es privado ver nota abajo)
RUN git clone --depth 1 --branch $REPO_BRANCH $REPO_URL . \
    && git lfs pull --include="services/app/data/modelo_multilabel.pkl" || true

# mostrar tamaño del archivo para debugging durante build
RUN ls -lh services/app/data/modelo_multilabel.pkl || true

# instalar dependencias (ajusta path al requirements correcto)
RUN pip install --no-cache-dir --upgrade -r services/requirements.txt

WORKDIR /code/services
EXPOSE 8004

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004", "--reload"]

