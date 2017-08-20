from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember, forget
from ..services.user import UserService
from ..forms import RegistrationForm
from ..models.user import User
from ..services.question_record import QuestionRecordService


# ROUTES IN ACTIVE USE ---
@view_config(route_name='home',
             renderer='pyramid_blogr:templates/register.jinja2')
@view_config(route_name='register-success',
             renderer='pyramid_blogr:templates/register-success.jinja2')
@view_config(route_name='register-error',
             renderer='pyramid_blogr:templates/register-error.jinja2')
def index_page(request):
    # template logic
    page = int(request.params.get('page', 1))
    paginator = QuestionRecordService.get_paginator(request, page)
    # get author names
    author_list = UserService.all_users(request)
    # why is ther a lambda here? what is lambda? https://stackoverflow.com/questions/2827623/python-create-object-and-add-attributes-to-it - atm to pdm
    for item in paginator.items:
        item.author = lambda: None
        item.author = author_list[item.user_id-1].name    # sign-in form
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        # ensure no duplicate is sent to db
        tempname = form.username.data
        flag = request.dbsession.query(User).filter_by(name=tempname).all()
        if flag:
            return HTTPFound(location=request.route_url('register-error'))
        # create account logic
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf8'))
        request.dbsession.add(new_user)
        # if all is successful
        headers = remember(request, tempname)
        return HTTPFound(location=request.route_url('register-success'), headers=headers)
    return {'form': form, 'paginator': paginator}


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
    return HTTPFound(location=request.route_url('question'), headers=headers)


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
