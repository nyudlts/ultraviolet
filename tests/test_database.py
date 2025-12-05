import psycopg2
from invenio_accounts.models import User


def test_database():
    conn = psycopg2.connect(
        dbname="invenio",
        user="invenio",
        password="invenio",
        host="localhost"
    )

    assert conn is not None


def test_db1(db):
    db.session.add(User(username='alice'))
    db.session.commit()
    assert User.query.count() == 1
