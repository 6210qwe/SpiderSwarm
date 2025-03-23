
class TransformTypeError(TypeError):
    pass


class OutputError(Exception):
    pass

class SpiderTypeError(TypeError):
    pass

class ItemInitError(Exception):
    pass

class ItemAttributeError(Exception):
    pass

class DecodeError(Exception):
    pass

class MiddlewareInitError(Exception):
    pass

class InvalidOutput(Exception):
    pass

class PipelineInitError(Exception):
    pass

class RequestMethodError(Exception):
    pass

class IgnoreRequest(Exception):
    def __init__(self, *args: object):
        super().__init__(args)
        self.msg = None

    pass