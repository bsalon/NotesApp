import Database


class BaseService:
    """
    Basic operations on the model
    """

    def __init__(self, service_model, *args, **kwargs):
        """
        Initializes service and saves the model
        """

        self.model = service_model


    def create(self, **keys_values):
        """
        Create Model instance

        :return: Return value of the query
        """

        return self.model.create(**keys_values)


    def delete(self, instance):
        """
        Delete Model instance

        :param instance: Instance to be deleted

        :return: Return value of the query
        """

        return instance.delete_instance()


    def update(self, **keys_values):
        """
        Update Model instance

        :return: Return value of the query
        """

        return self.model.update(**keys_values)


    def paginate(self, page, size):
        """
        Gets size amount of Model instances

        :param page: Page of the pagination
        :param size: Size of the page

        :return: Size amount of Model instances 
        """

        return self.model.select().paginate(page, size)
    

    def exists_by_name(self, name):
        """
        Checks if Model instance with name exists

        :param name: Model instance name

        :return: True if Model instance with name exists False otherwise
        """

        return self.model.select().where(self.model.name == name).exists()


    def get_by_id(self, item_id):
        """
        Gets Model instance with given id

        :param item_id: Model instance id

        :return: Model instance with given id
        """

        return self.model.select().where(self.model.id == item_id).get()

    
    def get_by_name(self, name):
        """
        Gets Model instance with given name

        :param item_id: Model instance name

        :return: Model instance with given name
        """

        return self.model.select().where(self.model.name == name).get()


    def get_all(self):
        """
        Gets Model instances

        :return: All Model instances
        """

        return self.model.select()


    def find_all_by_name(self, name):
        """
        Gets Model instances containing name substring

        :param name: Name substring

        :return: All Model instances with matching name
        """

        return self.model.select().where(self.model.name.contains(name))

