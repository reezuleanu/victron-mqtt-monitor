FROM python:3.11.11 as builder

WORKDIR /app

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY . /app

# compile project into a python package
RUN uv pip install --no-cache hatchling build \
  && python -m build --wheel

FROM python:3.11.11-slim

WORKDIR /app

# install compiled package
COPY --from=builder /app/dist/*.whl .

RUN pip install --no-cache-dir *.whl && rm *.whl
RUN apt update
RUN apt install -y curl

# disable docker log buffering
ENV PYTHONUNBUFFERED=1

ENV HOST=0.0.0.0
ENV PORT=8000

HEALTHCHECK --interval=1m --timeout=5s \
  CMD curl -f http://localhost:$PORT/health || exit 1

CMD python -m uvicorn victron_mqtt_monitor.bootloader:app --host $HOST --port $PORT