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
        # arrange paginator question set
        if(request.matchdict):
            # sort by user question sets
            keyset = int(request.matchdict.get('user_id',-1))
            if keyset != -1:
                query = query.filter(QuestionRecord.user_id == keyset)
            # send back question is selected ordee
            keyorder = request.matchdict.get('order', -1)
            if keyorder == 'mostrecent':
                query = query.order_by(sa.desc(QuestionRecord.created))
            elif keyorder == 'leastrecent':
                query = query.order_by(sa.asc(QuestionRecord.created))
            query_params = request.GET.mixed() 
        def url_maker(link_page):
            # replace page param with values generated by paginator
            query_params['page'] = link_page
            return request.current_route_url(_query=query_params)
        return SqlalchemyOrmPage(query, page, items_per_page=40,
                                 url_maker=url_maker)
