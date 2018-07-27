
[![Build Status](https://travis-ci.org/michael-basweti/michael-basweti.github.io.svg?branch=dev-trial)](https://travis-ci.org/michael-basweti/michael-basweti.github.io)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/codeclimate/codeclimate/test_coverage)

## MyDiary
This is a backend API for a diary where one can be able to make entries for each day and can get reminders to make an entry daily

## API ROUTES

| Methods        | Url          | Description |
| ------------- |:-------------:| -----:|
| GET     | http://127.0.0.1:5000/v1/entries/          |  Fetches all diary entries |          
| GET     | http://127.0.0.1:5000/v1/entries/<int:id>  |  Fetches a single diary entry    |
| POST    | http://127.0.0.1:5000/v1/entries/          |  Creates a new diary entry       |
| PUT     | http://127.0.0.1:5000/v1/entries/<int:id>  |   Modifies an entry              |
| DELETE  | http://127.0.0.1:5000/v1/entries/<int:id>  |   Deletes an entry from my Diary |


## USAGE

```
git clone https://github.com/michael-basweti/michael-basweti.github.io.git

## Go into the the directory you have cloned using the following command

cd michael-basweti.github.io.git

in the command create virtual env using the following commands

vitualenv venv

activate the environment:

venv/Scripts/activate   #windows guys
venv/bin/activate  #linux guys




```
