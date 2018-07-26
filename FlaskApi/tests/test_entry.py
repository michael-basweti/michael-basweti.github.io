"""
nose tests for the api
"""
import requests
from nose.tools import assert_true,assert_false



def test_get_all():
    """
    test all returns
    :return:
    """
    response = requests.get('http://127.0.0.1:5000/mydiary/v1/entries/')
    assert_true(response.ok)


def test_post():
    """
    test post
    :return:
    """
    response = requests.post('http://127.0.0.1:5000/mydiary/v1/entries/')
    assert_true(response.ok)


def test_get_one():
    """
    test get one
    :return:
    """
    response = requests.get('http://127.0.0.1:5000/mydiary/v1/entries/1')
    assert_true(response.ok)


def test_edit_one():
    """
    test editing
    :return:
    """
    response = requests.put('http://127.0.0.1:5000/mydiary/v1/entries/1')
    assert_true(response.ok)


def test_delete_one():
    """
    test delete
    :return:
    """
    response = requests.delete('http://127.0.0.1:5000/mydiary/v1/entries/1')
    assert_true(response.ok)
