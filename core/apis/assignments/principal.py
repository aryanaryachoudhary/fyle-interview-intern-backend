#Added by me

from flask import Blueprint, jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher

from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema
principal_assignment_resources = Blueprint('principal_assignment_resources', __name__)


@principal_assignment_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of submitted and graded assignments"""
    assignments = Assignment.get_all_submitted_and_graded()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_assignment_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""
    teachers = Teacher.get_all()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)


# @principal_assignment_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def grade_assignment(p, incoming_payload):
#     """Grade or re-grade an assignment"""
#     grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

#     graded_assignment = Assignment.mark_grade(
#         _id=grade_assignment_payload.id,
#         grade=grade_assignment_payload.grade,
#         auth_principal=p
#     )
#     db.session.commit()
#     graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
#     return APIResponse.respond(data=graded_assignment_dump)
@principal_assignment_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Fetch the assignment first
    assignment_to_grade = Assignment.query.get(grade_assignment_payload.id)

    if not assignment_to_grade:
        return jsonify({'error': 'Assignment not found'}), 404

    # Check if the assignment is in 'DRAFT' state
    if assignment_to_grade.state == 'DRAFT':
        return APIResponse.respond(error="Assignment is in draft state and cannot be graded", status_code=400)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

