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





@pytest.fixture
def test_grade_assignment_draft_assignment(client, h_principal, setup_draft_assignment):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,  
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

    assert response.status_code == 404  

def test_grade_assignment_invalid_grade(client, h_principal):
    """
    failure case: If an invalid grade is provided, the request should fail
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 1,
            'grade': 'INVALID_GRADE'  
        },
        headers=h_principal
    )

    assert response.status_code == 400  

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
        headers=h_student_1  
    )

    assert response.status_code == 403  
