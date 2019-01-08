from ..models.user import User


class UserService(object):

    @classmethod
    def by_name(cls, name, request):
        return request.dbsession.query(User).filter(User.name == name).first()

    @classmethod
    def all_users(cls, request):
        return request.dbsession.query(User)
