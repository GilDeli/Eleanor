from src.core.interfaces import PipelineHandler

class PipelineBase(PipelineHandler):
    def __init__(self,input_type,output_type):
        if (self._init_type):
            raise RuntimeError("The value has already been initialized via a generic")
        else:
            self._input_type = input_type
            self._output_type = output_type
