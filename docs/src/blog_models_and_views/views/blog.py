from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from ..models.blog_record import BlogRecord
from ..services.blog_record import BlogRecordService


@view_config(route_name='blog',
             renderer='graphwhy:templates/view_blog.jinja2')
def blog_view(request):
    blog_id = int(request.matchdict.get('id', -1))
    entry = BlogRecordService.by_id(blog_id, request)
    if not entry:
        return HTTPNotFound()
    return {'entry': entry}


@view_config(route_name='blog_action', match_param='action=create',
             renderer='graphwhy:templates/edit_blog.jinja2')
def blog_create(request):
    return {}


@view_config(route_name='blog_action', match_param='action=edit',
             renderer='graphwhy:templates/edit_blog.jinja2')
def blog_update(request):
    return {}
