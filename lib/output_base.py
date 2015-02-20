import abc

class OutputBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def set(self, data):
        return

    @abc.abstractmethod
    def save(self):
        return


