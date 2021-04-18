import json


class Config(object):
    """
    This class manages configurations.
    This is a singleton class.
    """

    __species = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self):
        if self.__first_init:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.configs = json.load(f)
                f.close()
            self.__class__.__first_init = False

    def update(self):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.configs, f, ensure_ascii=False)
            f.close()

    def over_write(self, new_configs):
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(new_configs, f, ensure_ascii=False)
            f.close()
        self.configs = new_configs

    def __str__(self):
        return "Configurations: %s" % self.configs
