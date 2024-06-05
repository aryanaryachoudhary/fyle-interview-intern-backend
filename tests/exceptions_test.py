#Added by me
import pytest
from core.libs.exceptions import FyleError

def test_fyle_error_initialization():
    error = FyleError(404, "Resource not found")
    assert error.status_code == 404
    assert error.message == "Resource not found"

def test_fyle_error_default_status_code():
    error = FyleError(FyleError.status_code, "Default error")
    assert error.status_code == 400
    assert error.message == "Default error"

def test_fyle_error_to_dict():
    error = FyleError(500, "Server error")
    error_dict = error.to_dict()
    assert error_dict == {'message': "Server error"}

def test_fyle_error_inheritance():
    error = FyleError(401, "Unauthorized")
    assert isinstance(error, Exception)

def test_fyle_error_without_message():
    error = FyleError(403, None)
    assert error.to_dict() == {'message': None}
