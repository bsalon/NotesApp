class BaseService:
    def __init__(self, service_model, *args, **kwargs):
        self.model = service_model


    def create(self, **keys_values):
        return self.model.create(**keys_values)


    def delete(self, instance):
        return instance.delete_instance()


    def update(self, **keys_values):
        return self.model.update(**keys_values)


    def paginate(self, page, size):
        return model.select().paginate(page, size)

