from BusinessLogic.BaseService import BaseService

from Models.Tag import TagModel


class TagService(BaseService):
    def __init__(self):
        super().__init__(TagModel)


    def update_tag(self, tag, updated_tag):
        return TagModel \
            .update(name = updated_tag.name, \
                description = updated_tag.description) \
            .where(TagModel.id == tag.id) \
            .execute()

