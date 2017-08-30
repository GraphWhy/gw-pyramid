from ..services.user import UserService
from ..services.question_record import QuestionRecordService


class QuestionTemplateService(object):

    @classmethod
    def author_names(cls, request):
        page = int(request.params.get('page', 1))
        paginator = QuestionRecordService.get_paginator(request, page)
        author_list = UserService.all_users(request)
        for item in paginator.items:
            item.author = author_list[item.user_id - 1].name
        return paginator



