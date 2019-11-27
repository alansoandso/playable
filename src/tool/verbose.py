class Verbose(object):
    __state = False

    def status(self):
        return Verbose.__state

    def set(self):
        Verbose.__state = True

    def unset(self):
        Verbose.__state = False

    def output(self, string, **kwargs):
        if Verbose.__state:
            print(string, kwargs)


if __name__ == '__main__':
    # Verbose().set()
    # w = Verbose()
    # w.unset()

    if Verbose().status():
        print('True')
        Verbose().output('show when true')
    else:
        print('False')
        Verbose().output('Error show when false')
