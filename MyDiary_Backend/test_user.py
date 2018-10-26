"""
nose tests for the api
"""
from nose.tools import assert_true
import requests


def test_get_all():
    """
    test all returns
    :return:
    """
    response = requests.get('http://127.0.0.1:5000/mydiary/api/v1.0/entries/get')
    assert_true(response.ok)


def test_post():
    """
    test post
    :return:
    """
    response = requests.post('http://127.0.0.1:5000/mydiary/api/v1.0/entries/post')
    assert_true(response.ok)


def test_get_one():
    """
    test get one
    :return:
    """
    response = requests.get('http://127.0.0.1:5000/mydiary/api/v1.0/entries/get/1')
    assert_true(response.ok)


def test_edit_one():
    """
    test editing
    :return:
    """
    response = requests.put('http://127.0.0.1:5000/mydiary/api/v1.0/entries/edit/1')
    assert_true(response.ok)


def test_delete_one():
    """
    test delete
    :return:
    """
    response = requests.delete('http://127.0.0.1:5000/mydiary/api/v1.0/entries/delete/1')
    assert_true(response.ok)
