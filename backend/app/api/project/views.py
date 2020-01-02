from itertools import chain

from flask import request

from . import project
from ... import db
from ...models import Project
from ...libs.error_code import OK, ParamsError
from ...decorators import login_required


@project.route('/get-list')
@login_required
def get_projects(current_user):
    """获取项目列表。"""
    projects = []
    department_id = request.args.get('department_id')

    for p in chain(
            Project.query
                    .filter(Project.enable)
                    .filter(Project.department_id == department_id)
                    .filter(Project.masters.contains(current_user))
                    .all(),
            Project.query
                    .filter(Project.enable)
                    .filter(Project.department_id == department_id)
                    .filter(Project.users.contains(current_user))
                    .all()
    ):
        projects.append({
            'id': p.id,
            'name': p.name
        })

    return OK(projects=projects)


@project.route('/get-info')
@login_required
def get_project_info(current_user):
    """获取项目信息。"""
    project_id = request.args.get('project_id')
    project_name = request.args.get('project_name')
    if project_id:
        p = Project.query.get(project_id)
    elif project_name:
        p = Project.query.filter_by(name=project_name).first()
    else:
        raise ParamsError

    return OK(project={
        'id': p.id,
        'name': p.name,
        'masters': [u.username for u in p.masters.all()],
        'users': [u.username for u in p.users.all()]
    })


@project.route('/set-active-project', methods=['POST'])
@login_required
def set_active_project(current_user):
    """设置活动项目。"""
    project_name = request.json.get('project_name')
    p = Project.query.filter_by(name=project_name).first()
    current_user.active_project = p
    db.session.commit()

    return OK()
