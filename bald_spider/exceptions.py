
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
    pass

class NotConfigured(Exception):
    pass

class ExtensionInitError(Exception):
    pass

class ReceiverTypeError(Exception):
    pass