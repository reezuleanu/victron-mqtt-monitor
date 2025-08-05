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

# update keys
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg ca-certificates

RUN pip install --no-cache-dir *.whl && rm *.whl

CMD ["python", "-m", "victron_mqtt_monitor.main"]