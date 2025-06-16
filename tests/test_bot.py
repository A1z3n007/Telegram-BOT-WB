import pytest
from types import SimpleNamespace as namespace
from core import analyze_article
from utils import bool_1
from database import init_db

init_db()

@pytest.fixture
def authorized_user():
    return namespace(chat=namespace(id=1795671737), text="272181996")

def test_start_authorized():
    message = namespace(chat=namespace(id=1795671737))
    assert bool_1(message) == True

def test_start_unauthorized():
    message = namespace(chat=namespace(id=1234567890))
    assert bool_1(message) == False

@pytest.mark.parametrize("article", ["272181996", "31372372"])
def test_valid_articles(authorized_user, article):
    authorized_user.text = article
    try:
        analyze_article(None, authorized_user)
    except Exception as e:
        pytest.fail(f"analyze_article вызвал исключение: {e}")
