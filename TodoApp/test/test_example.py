import pytest

# /**************************************************** Pytest Basics **************************************************************/


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1


def test_is_instance():
    assert isinstance('Hello World!', str)
    assert not isinstance('10', int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False


def test_type():
    assert type('Hello World!' is str)
    assert type('10'is not int)

def test_greater_and_less_than():
    assert 7 > 3
    assert 4 < 10

def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)


# /**************************************************** Pytest Objects **************************************************************/

class Student():
    def __init__(self, first_name, last_name, major, years):
        self.first_name = first_name,
        self.last_name = last_name,
        self.major = major,
        self.years = years


# Old way pytest.fixture can be used to use the same python object in multiple test functions
# def test_person_initialization():
#     p = Student('John', 'Doe', 'Computer Science', 3)
#     assert p.first_name == 'John', 'First name should be John'
#     assert p.second_name == 'Doe', 'Second name should be Doe'
#     assert p.major == 'Computer Science'
#     assert p.years == 3


@pytest.fixture
def default_student():
    return Student('John', 'Doe', 'Computer Science', 3)


def test_person_initialization(default_student):
    assert default_student.first_name == ('John',), 'First name should be John'
    assert default_student.last_name == ('Doe',), 'Second name should be Doe'
    assert default_student.major == ('Computer Science',)
    assert default_student.years == 3






