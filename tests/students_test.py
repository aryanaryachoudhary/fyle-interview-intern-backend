def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'
    

#Added by me

def test_create_assignment_invalid_data(client, h_student_1):
    """
    failure case: If invalid data is provided, the request should fail
    """
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': 123  # Invalid content
        })

    assert response.status_code == 400  # Assuming your API returns 400 for bad requests

def test_submit_nonexistent_assignment(client, h_student_1):
    """
    failure case: If an assignment does not exist, it cannot be submitted
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 9999,  # Assuming this ID does not exist
            'teacher_id': 1
        })

    assert response.status_code == 404  # Assuming your API returns 404 for non-existent resources

def test_submit_assignment_without_permission(client, h_teacher_1):
    """
    failure case: If a user without the necessary permissions tries to submit an assignment, the request should fail
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_teacher_1,  # Teacher trying to submit an assignment
        json={
            'id': 1,
            'teacher_id': 1
        })

    assert response.status_code == 403  # Assuming your API returns 403 for forbidden actions

