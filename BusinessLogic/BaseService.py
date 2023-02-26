import Database


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
        return self.model.select().paginate(page, size)
    

    def exists_by_name(self, name):
        return self.model.select().where(self.model.name == name).exists()


    def get_by_id(self, item_id):
        return self.model.select().where(self.model.id == item_id).get()

    
    def get_by_name(self, name):
        return self.model.select().where(self.model.name == name).get()


    def get_all(self):
        return self.model.select()
