from flask import Blueprint, jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)   #Updated by me
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


#Updated by me

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Fetch the assignment first
    assignment_to_grade = Assignment.query.get(grade_assignment_payload.id)

    if not assignment_to_grade:
        return jsonify({'error': 'Assignment not found'}), 404

    # Check if the assignment was submitted to the current teacher
    if assignment_to_grade.teacher_id != p.teacher_id:
        return jsonify({'error': 'FyleError'}), 400

    # Check if the assignment is in 'DRAFT' state
    if assignment_to_grade.state == 'DRAFT':
        return jsonify({'error': 'FyleError'}), 400

    # Check if the assignment has already been graded
    if assignment_to_grade.state == 'GRADED':
        return jsonify({'error': 'FyleError'}), 400

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

