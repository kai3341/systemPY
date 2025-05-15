from celery import Celery, signals  # type: ignore[import-untyped]
from typing_extensions import deprecated

from systempy import Target


@deprecated("Will be removed into separated package")
class CeleryUnit(Target):
    celery_app: Celery | type[Celery]
    config: dict

    def on_init(self) -> None:
        signals.worker_init.connect(self.pre_startup)
        signals.worker_ready.connect(self.pre_startup)
        signals.worker_shutting_down.connect(self.on_shutdown)
        signals.worker_shutdown.connect(self.post_shutdown)

    def pre_startup(self) -> None:
        obj: dict = self.config["Celery"]
        self.celery_app.config_from_object(obj)
