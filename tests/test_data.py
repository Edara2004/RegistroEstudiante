import pytest
from source.admin_data_student.dataquery import DataQuery
from source.admin_data_student.time_function import time_register


@pytest.fixture
def data_queries():
    db_dir: str = 'source/data_student.db'
    db_test = DataQuery(db_dir)
    yield db_test
    db_test.close_database(db_test.connect_data_base())


def test_insert_data(data_queries):
    connection = data_queries.connect_data_base()
    id_student = 18934523
    name = 'Pedro Marquez'
    birthday = '2002-15-05'
    nationality = 'Panameña'
    gender = 'Masculino'
    email = 'eduar@gmail.com'
    register = 'Si'
    semester = 1.0
    career = 'Sistemas'
    time = time_register()

    data_queries.insert_student(connection, id_student, name, birthday, nationality, gender, email,
                                register, semester, career, time)

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM data_student')
    register_data = cursor.fetchone()

    assert register_data[0] == 18934523
    assert register_data[1] == name
    assert register_data[2] == birthday
    assert register_data[3] == nationality
    assert register_data[4] == gender
    assert register_data[5] == email
    assert register_data[6] == register
    assert register_data[7] == semester
    assert register_data[8] == career
    assert register_data[9] == time

    data_queries.close_database(connection)
