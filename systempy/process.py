from . import target


class ProcessUnit(target.ProcessTargetABC):
    def run_sync(self):
        with self:
            self.main_sync()
