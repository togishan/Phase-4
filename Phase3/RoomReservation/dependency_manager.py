class DependencyManager:
    objects = {}

    @staticmethod
    def register(type: type, obj) -> None:
        DependencyManager.objects[type] = obj

    @staticmethod
    def get(type: type) -> object | None:
        return DependencyManager.objects[type]

    @staticmethod
    def unregister(type: type) -> None:
        del DependencyManager.objects[type]
