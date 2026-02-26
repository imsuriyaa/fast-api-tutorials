import pytest

# Validate Integers
def test_equal_or_not_equal():
    assert 1 == 1
    assert 1 != 2

def get_student():
    return Student("John", "Doe", "Computer Science", 4)

# Validate Instances
def test_instance():
    assert isinstance(1, int)
    assert isinstance("hello", str)
    assert isinstance(get_student(), Student)

# Validate Greater than & less than
def test_greater_than_or_less_than():
    assert 1 > 0
    assert 1 < 2
    assert not (1 > 2)
    assert not (1 < 0)

# Validate Boolean
def test_boolean():
    validate = True
    assert validate is True
    assert ('hello'=='world') is False

# Validate List
def test_list():
    assert [1, 2, 3] == [1, 2, 3]
    assert [1, 2, 3] != [1, 2, 4]
    assert len([1, 2, 3]) == 3
    assert 1 in [1, 2, 3]
    assert 4 not in [1, 2, 3]


# Validate Type
def test_type():
    assert type(1) is int
    assert type("hello") is str
    assert not type(1) is str
    assert type(['1','2','3']) is list
    assert type({'name':'John', 'age':30}) is dict
    assert type((1,2,3)) is tuple
    assert type({1,2,3}) is set
    

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_student():
    return Student("John", "Doe", "Computer Science", 4)

def test_student_initialization(default_student):
    assert default_student.first_name == "John"
    assert default_student.last_name == "Doe"
    assert default_student.major == "Computer Science"
    assert default_student.years == 4



