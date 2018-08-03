"""
nose tests for the api
"""
from nose.tools import assert_false,assert_false
import requests


def test_login():
    """
    test all returns
    :return:
    """
    response = requests.get('http://127.0.0.1:5000/user/v1/actions/login')
    assert_false(response.ok)


def test_register():
    """
    test post
    :return:
    """
    response = requests.post('http://127.0.0.1:5000/user/v1/actions/registration')
    assert_false(response.ok)


def delete_user():
    """
    test get one
    :return:
    """
    response = requests.get('http://127.0.0.1:5000/user/v1/actions/delete/2')
    assert_false(response.ok)


def edit_user():
    """
    test editing
    :return:
    """
    response = requests.put('http://127.0.0.1:5000/user/v1/actions/user/update/3')
    assert_false(response.ok)


def get_all_users():
    """
    test delete
    :return:
    """
    response = requests.delete('http://127.0.0.1:5000/user/v1/actions/users')
    assert_false(response.ok)


def get_one_user():
    """
    test delete
    :return:
    """
    response = requests.delete('http://127.0.0.1:5000/user/v1/actions/users/3')
    assert_false(response.ok)
