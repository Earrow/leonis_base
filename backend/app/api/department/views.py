from itertools import chain

from . import department
from ...models import Department, User
from ...libs.error_code import OK
from ...decorators import login_required


def _pack_department(d: Department, user: User):
    """打包部门对象，返回部门名称和包含该用户的子部门列表。

    :param d: 部门对象。
    :param user: 用户对象，用户必须属于:param:`d`部门，返回的子部门也都是包含该用户的。
    :return: 部门数据字典，包括id、名称和子部门列表。
    """
    if not (user in d.users or user in d.masters):
        raise AttributeError(f'{user}不属于{d}')

    ret = {
        'id': d.id,
        'name': d.name,
        'children': []
    }
    for child_department in chain(d.child_departments
                                          .filter(Department.enable)
                                          .filter(Department.masters.contains(user))
                                          .all(),
                                  d.child_departments
                                          .filter(Department.enable)
                                          .filter(Department.users.contains(user))
                                          .all()
                                  ):
        ret['children'].append(_pack_department(child_department, user))

    return ret


@department.route('/get-list')
@login_required
def get_departments(current_user):
    """获取部门列表。"""
    departments = []
    for top_department in chain(Department.query
                                        .filter(Department.is_top)
                                        .filter(Department.enable)
                                        .filter(Department.masters.contains(current_user))
                                        .all(),
                                Department.query
                                        .filter(Department.is_top)
                                        .filter(Department.enable)
                                        .filter(Department.users.contains(current_user))
                                        .all()
                                ):
        departments.append(_pack_department(top_department, current_user))

    return OK(departments=departments)
