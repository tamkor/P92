class ConfigReaderError(Exception):
    def __init__(self,
                 msg="Something went wrong while handling the config.json file.",
                 *args,
                 **kwargs):
        super().__init__(msg, *args, **kwargs)
