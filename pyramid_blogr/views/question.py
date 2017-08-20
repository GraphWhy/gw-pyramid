from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from ..models.user import User
from ..models.question_record import QuestionRecord
from ..services.question_record import QuestionRecordService
from ..forms import QuestionCreateForm, QuestionUpdateForm



@view_config(route_name='question',
             renderer='pyramid_blogr:templates/view_question.jinja2')
def question_view(request):
    question_id = int(request.matchdict.get('id', -1))
    entry = QuestionRecordService.by_id(question_id, request)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(route_name='question_action', match_param='action=create',
             renderer='pyramid_blogr:templates/edit_question.jinja2',
             permission='create')
def question_create(request):
    # template logic
    page = int(request.params.get('page', 1))
    paginator = QuestionRecordService.get_paginator(request, page)
    # question logic
    entry = QuestionRecord()
    form = QuestionCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        query = request.dbsession.query(User)
        query = query.filter(User.name == request.authenticated_userid).first()
        setattr(entry, 'user_id', query.id)
        request.dbsession.add(entry)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form, 'action': request.matchdict.get('action'), 'paginator': paginator}


@view_config(route_name='question_action', match_param='action=edit',
             renderer='pyramid_blogr:templates/edit_question.jinja2',
             permission='create')
def question_update(request):
    question_id = int(request.params.get('id', -1))
    entry = QuestionRecordService.by_id(question_id, request)
    if not entry:
        return HTTPNotFound()
    form = QuestionUpdateForm(request.POST, entry)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        return HTTPFound(
            location=request.route_url('question', id=entry.id, slug=entry.slug))
    return {'form': form, 'action': request.matchdict.get('action')}
