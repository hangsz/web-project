FROM python:3.12.12-bookworm

ENV APP_ENV=LOCAL

# 创建非root用户和组
RUN groupadd -r admin && useradd -r -g admin admin
RUN mkdir -p /home/admin/logs && mkdir -p /home/admin/scripts

COPY --chown=admin:admin scripts /home/admin/scripts
RUN chmod -R +x /home/admin/scripts


COPY --chown=admin:admin pyproject.toml /home/admin/app/
COPY --chown=admin:admin uv.lock /home/admin/app/
RUN cd /home/admin/app && \
    python3 -m venv .venv && \
    . .venv/bin/activate && \ 
    pip install uv &&\
    uv sync


COPY --chown=admin:admin src /home/admin/app/src
COPY --chown=admin:admin tests /home/admin/app/tests

RUN chown admin:admin -R /home/admin

USER admin
WORKDIR /home/admin
ENTRYPOINT [ "bash", "/home/admin/scripts/start.sh"]