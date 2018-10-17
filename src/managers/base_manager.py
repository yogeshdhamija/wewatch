class BaseManager(object):
    def __init__(self, db):
        self.db = db

    def check_type(self, inpt, typ):
        return isinstance(inpt, typ)

    def check_type_or_raise(self, inpt, typ, message="Wrong Type"):
        if not self.check_type(inpt, typ):
            raise TypeError(message)
