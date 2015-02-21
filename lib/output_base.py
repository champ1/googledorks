import abc

#---------------------------------------------#
# Base Class for all the different medium of  #
#               output.                       #
# @author Amar Myana amar92@outlook.com       #  
#---------------------------------------------#
class OutputBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def set(self, data):
        return

    @abc.abstractmethod
    def save(self):
        return

    @abc.abstractmethod
    def getLastDork(self):
        return
