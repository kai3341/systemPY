from .target import ProcessTargetABC


class ProcessUnit(ProcessTargetABC):
    def run_sync(self):
        with self:
            self.main_sync()
