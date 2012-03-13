import os
import sys

from .collection import Collection
from .exceptions import CollectionNotFound
from .task import Task


class Loader(object):
    def __init__(self, root=None):
        """
        Creates a loader object with search root directory of ``root``.

        If not given, ``root`` defaults to ``os.getcwd``.
        """
        self.root = root or os.getcwd()

    def load_collection(self, name):
        c = Collection()
        parent = os.path.abspath(self.root)
        # If we want to auto-strip .py:
        # os.path.splitext(os.path.basename(name))[0]
        # TODO: copy over rest of path munging from fabric.main
        if parent not in sys.path:
            sys.path.insert(0, parent)
        try:
            module = __import__(name)
            candidates = filter(
                lambda x: getattr(x[1], 'is_invoke_task', False),
                vars(module).items()
            )
            if not candidates:
                # Recurse downwards towards FS
                pass
            for name, task in candidates:
                c.add_task(name, task)
            return c
        except ImportError, e:
            raise CollectionNotFound(name=name, root=self.root, error=e)