class ConfigReaderError(Exception):
    def __init__(self,
                 msg="The config.json in the project with 'http' and 'websocket' keys are required!",
                 *args,
                 **kwargs):
        super().__init__(msg, *args, **kwargs)
