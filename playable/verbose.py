class Verbose(object):
    __level = 0

    def level(self):
        return Verbose.__level

    def set(self, level=1):
        Verbose.__level = level

    def unset(self):
        Verbose.__level = 0

    def output(self, string, verbosity=0, **kwargs):
        """
        Default message verbosity is 0 and level is 0 so output is suppressed
        until level is set to 1 or above
        """
        if verbosity < Verbose.__level:
            print(string, **kwargs)

