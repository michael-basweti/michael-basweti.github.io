import unittest
import json
import os
import pytest
from flask import Flask
from nose.tools import assert_true
from manage import app
from flask_testing import TestCase
import requests



def test_get_all():
    response = requests.get('http://127.0.0.1:5000/mydiary/api/v1.0/entries/get')
    assert_true(response.ok)

def test_post():
    response = requests.post('http://127.0.0.1:5000/mydiary/api/v1.0/entries/post')
    assert_true(response.ok)

def test_get_one():
    response = requests.get('http://127.0.0.1:5000/mydiary/api/v1.0/entries/get/1')
    assert_true(response.ok)

def test_edit_one():
    response = requests.put('http://127.0.0.1:5000/mydiary/api/v1.0/entries/edit/1')
    assert_true(response.ok)

def test_delete_one():
    response = requests.delete('http://127.0.0.1:5000/mydiary/api/v1.0/entries/delete/1')
    assert_true(response.ok)