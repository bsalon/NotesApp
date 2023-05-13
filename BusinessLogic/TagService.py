from BusinessLogic.BaseService import BaseService

from Models.Tag import TagModel


class TagService(BaseService):
    """
    Tag operations
    """

    def __init__(self):
        super().__init__(TagModel)


    def update_tag(self, tag, updated_tag):
        """
        Updates tag with new tag values

        :param tag: Old tag
        :param updated_tag: New tag values

        :return: Return value of the query
        """

        return TagModel \
            .update(name = updated_tag.name, \
                description = updated_tag.description) \
            .where(TagModel.id == tag.id) \
            .execute()

