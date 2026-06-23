FROM python:3.11-slim AS base

# CISO Directive: Atualização de pacotes de segurança e criação de usuário sem privilégios
RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    groupadd -g 10001 aegis_group && \
    useradd -m -u 10001 -g aegis_group aegis_user

WORKDIR /opt/aegis

# Instalação de dependências de forma isolada
COPY --chown=aegis_user:aegis_group requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cópia do código-fonte com permissões estritas
COPY --chown=aegis_user:aegis_group src/ ./src/

# CISO Directive: Drop para usuário não-root (Rootless Container)
USER aegis_user

# Proteção contra gravação indevida no runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-m", "src.middleware"]
