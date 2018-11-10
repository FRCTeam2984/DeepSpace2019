class Singleton(type):
    r"""A metaclass that is to be inherited by any class that wants
        to be a singleton. When the inheriting class is called,
        it runs the __call__ method, checking if it has already 
        been called and, if so, returns that instance"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Checks if the ineriting class has already been called,
            and returns the previously made instance if so."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
