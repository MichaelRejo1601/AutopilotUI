class Node():
    instances = []
    def __init__(self, value):
        self.value = value
        self.children = []
        self.__class__.instances.append(self)

    def add_child(self, obj):
        self.children.append(obj)

    @classmethod
    def printInstances(cls):
        return cls.instances
