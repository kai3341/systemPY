from typing import Union, Type
from celery import Celery, signals  # type: ignore

from ..target import Target

from mypy_extensions import trait


@trait
class CeleryUnit(Target):
    celery_app: Union[Celery, Type[Celery]]
    config: dict

    def on_init(self) -> None:
        signals.worker_init.connect(self.pre_startup)
        signals.worker_ready.connect(self.pre_startup)
        signals.worker_shutting_down.connect(self.on_shutdown)
        signals.worker_shutdown.connect(self.post_shutdown)

    def pre_startup(self) -> None:
        self.celery_app.config_from_object(self.config["Celery"])
