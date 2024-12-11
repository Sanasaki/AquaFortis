class System:
    pass


class Task:
    pass


class Engine:
    pass


class Simulation:
    def __init__(self, system: System, task: Task, engine: Engine):
        self.system = system
        self.task = task
        self.engine = engine
