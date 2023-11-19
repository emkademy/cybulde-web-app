FROM python:3.10-slim

ENV HOME=/home/${USER_NAME} \
    VIRTUAL_ENV=/home/${USER_NAME}/venv
ENV \
  PYTHONUNBUFFERED=1 \
  DEBIAN_FRONTEND=noninteractive \
  TZ=Europe/Warsaw \
  PATH="/usr/local/gcloud/google-cloud-sdk/bin:${HOME}/.local/bin:${VIRTUAL_ENV}/bin:${PATH}" \
  PYTHONPATH="/app:${PYTHONPATH}" \
  BUILD_POETRY_LOCK="${HOME}/poetry.lock.build"

RUN apt-get -qq update \
    && apt-get -qq -y install vim gcc curl git build-essential libb64-dev software-properties-common \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean

RUN curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-426.0.0-linux-x86_64.tar.gz > /tmp/google-cloud-sdk.tar.gz
RUN mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh --usage-reporting false --command-completion true --bash-completion true --path-update true --quiet

RUN pip install mlflow==2.5.0 psycopg2-binary~=2.9

COPY ./docker/scripts/* /
RUN chmod +x /*.sh

CMD ["/start-mlflow-server.sh"]
