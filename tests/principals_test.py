import pytest
from core.models.assignments import AssignmentStateEnum, GradeEnum





def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]




# Use this fixture in your test
@pytest.fixture
def test_grade_assignment_draft_assignment(client, h_principal, setup_draft_assignment):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,  # Ensure that assignment with id 5 is in DRAFT state in your test setup
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400



def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


#Added by me
def test_grade_nonexistent_assignment(client, h_principal):
    """
    failure case: If an assignment does not exist, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 9999,  # Assuming this ID does not exist
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 404  # Assuming your API returns 404 for non-existent resources

def test_grade_assignment_invalid_grade(client, h_principal):
    """
    failure case: If an invalid grade is provided, the request should fail
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
            'grade': 'INVALID_GRADE'  # Invalid grade
        },
        headers=h_principal
    )

    assert response.status_code == 400  # Assuming your API returns 400 for bad requests

def test_grade_assignment_without_permission(client, h_student_1):
    """
    failure case: If a user without the necessary permissions tries to grade an assignment, the request should fail
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
            'grade': GradeEnum.A.value
        },
        headers=h_student_1  # Student trying to grade an assignment
    )

    assert response.status_code == 403  # Assuming your API returns 403 for forbidden actions
