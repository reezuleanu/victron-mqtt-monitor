from contextlib import asynccontextmanager
from threading import Thread

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from victron_mqtt_monitor.utils import init_logger, init_i18n
from victron_mqtt_monitor.settings import config
from victron_mqtt_monitor.api import router
from victron_mqtt_monitor.monitors.victron_monitor import VictronMonitor
from victron_mqtt_monitor.alerts.victron import BatteryAlert


init_logger(config.DEPLOYMENT, config.APP_NAME)
init_i18n(config.LOCALE)


monitor = VictronMonitor(
    config.BROKER_URL, config.VICTRON_ID, alerts=[BatteryAlert(0.85)]
)


monitor_thread = Thread(target=monitor.run, name="monitor_thread", daemon=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if config.APP_NAME:
        app.title = f"[{config.DEPLOYMENT.value}] {config.APP_NAME}"
    monitor_thread.start()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get("/health", tags=["health"])
def health(request: Request) -> JSONResponse:
    return JSONResponse({"detail": "ok"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
