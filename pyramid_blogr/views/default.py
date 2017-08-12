from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..services.user import UserService
from ..services.blog_record import BlogRecordService
from ..forms import RegistrationForm
from ..models.user import User


# ROUTES IN ACTIVE USE ---
@view_config(route_name='home',
             renderer='pyramid_blogr:templates/register.jinja2')
def index_page(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        tempname = form.username.data
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf8'))
        flag = request.dbsession.query(User).filter_by(name=tempname).all()
        if flag:
            return HTTPFound(location=request.route_url('register-error'))
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('thanks'))
    return {'form': form}


@view_config(route_name='register-error',
             renderer='pyramid_blogr:templates/register-error.jinja2')
def unique_error_page(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        tempname = form.username.data
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf8'))
        flag = request.dbsession.query(User).filter_by(name=tempname).all()
        if not flag:
            request.dbsession.add(new_user)
            return HTTPFound(location=request.route_url('thanks'))
        else:
            return HTTPFound(location=request.route_url('register-error'))
    return {'form': form}


@view_config(route_name='question',
             renderer='pyramid_blogr:templates/question.jinja2')
def question_page(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        tempname = form.username.data
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf8'))
        flag = request.dbsession.query(User).filter_by(name=tempname).all()
        if not flag:
            request.dbsession.add(new_user)
            return HTTPFound(location=request.route_url('thanks'))
        else:
            return HTTPFound(location=request.route_url('question'))
    return {'form': form}


@view_config(route_name='thanks',
             renderer='pyramid_blogr:templates/thanks.jinja2')
def thanks_page(request):
    form = RegistrationForm(request.POST)
    return {'form': form}


# ROUTES NOT IN USE ---
# ROUTES NOT IN USE ---
# ROUTES NOT IN USE ---

# original home view
# @view_config(route_name='home',
#             renderer='pyramid_blogr:templates/index.jinja2')
# def index_page(request):
#    page = int(request.params.get('page', 1))
#    paginator = BlogRecordService.get_paginator(request, page)
#    return {'paginator': paginator}


@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = UserService.by_name(username, request=request)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)


@view_config(route_name='register',
             renderer='pyramid_blogr:templates/register.jinja2')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf8'))
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}
