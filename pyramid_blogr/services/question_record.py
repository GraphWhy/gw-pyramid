import sqlalchemy as sa
from paginate_sqlalchemy import SqlalchemyOrmPage  # <- provides pagination
from ..models.question_record import QuestionRecord


class QuestionRecordService(object):

    @classmethod
    def all(cls, request):
        query = request.dbsession.query(QuestionRecord)
        return query.order_by(sa.desc(QuestionRecord.created))

    @classmethod
    def by_id(cls, _id, request):
        query = request.dbsession.query(QuestionRecord)
        return query.get(_id)

    @classmethod
    def get_paginator(cls, request, page=1):
        query = request.dbsession.query(QuestionRecord)
        query = query.order_by(sa.desc(QuestionRecord.created))
        query_params = request.GET.mixed()

        def url_maker(link_page):
            # replace page param with values generated by paginator
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)

        return SqlalchemyOrmPage(query, page, items_per_page=5,
                                 url_maker=url_maker)
