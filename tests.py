"""This is the main file with tests for the grocery shopping program"""

import pytest
import api
import json
from pathlib import Path

def test_show_all_dishes_in_database(return_test_database, capsys):
    """This is a test for the show_all function"""
    
    api.show_all()
    captured = capsys.readouterr()
    assert captured.out == 'Kapusniak \nPomidorowa \n'
    
def test_show_dish_which_is_in_the_database(return_test_database, monkeypatch, capsys):
    """This is a test for the show_dish function, for dish in database"""
    
    monkeypatch.setattr('builtins.input', lambda _: "Kapusniak")
    api.show_dish()
    captured = capsys.readouterr()
    assert captured.out == "The ingredients of Kapusniak are: ['kapusta', 'woda', 'mieso']\n"

def test_show_dish_which_is_not_in_the_database(return_test_database, monkeypatch, capsys):
    """This is a test for the show_dish function, for dish not in database"""
    
    monkeypatch.setattr('builtins.input', lambda _: "Grzybowa")
    api.show_dish()
    captured = capsys.readouterr()
    assert captured.out == "Dish Grzybowa doesn't exist in the database\n"

def test_remove_dish_from_database_which_is_not_in_the_database(return_test_database, monkeypatch, capsys):
    """Test the rm_dish function for dish which is not in the database"""
    
    monkeypatch.setattr('builtins.input', lambda _: "Grzybowa")
    api.rm_dish()
    captured = capsys.readouterr()
    assert captured.out == "Dish Grzybowa doesn't exist in the database\n"    

def test_remove_dish_from_database_which_is_in_the_database(return_test_database, monkeypatch, tmp_path, capsys):
    """Test the rm_dish function for dish which is in the database"""
    
    monkeypatch.setattr('builtins.input', lambda _: "Kapusniak")
    d = tmp_path / "sub"
    d.mkdir()
    monkeypatch.chdir(d)
    api.rm_dish()
    captured = capsys.readouterr()
    with open('database.json') as f:
        database = json.load(f)
    assert database == {"Pomidorowa":["pomidory", "woda", "mieso"]}
    assert captured.out == "Deleting dish Kapusniak\n"
    
def test_add_dish_which_is_already_in_the_database(return_test_database, monkeypatch, capsys):
    """Test the add dish function with dish which is already in the database"""
    
    monkeypatch.setattr('builtins.input', lambda _: "Kapusniak")
    api.add_dish()
    captured = capsys.readouterr()
    assert captured.out == "Dish Kapusniak already exists!\n"


@pytest.mark.skip    
def test_add_dish_which_is_not_yet_in_the_database(return_test_database, monkeypatch, capsys):
    """Test the add dish function with dish not yet in the database""" 


@pytest.fixture
def return_test_database(monkeypatch):
    """Fixture for returning test database"""
    
    def mockreturn():
        return {"Kapusniak":["kapusta", "woda", "mieso"],
        "Pomidorowa":["pomidory", "woda", "mieso"]}
    
    monkeypatch.setattr("api.open_database", mockreturn)
