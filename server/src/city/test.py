#!/usr/bin/env python

# Note :: Tests dogfooding City model for convenience
# For further decoupling independent utility (cleanup, selecting)
# methods could be implemented

from unittest import TestCase
from city.model import City, create, update

from database.mod import create_db_engine

def _create(conn, city):
    stmt = City.insert().values(city)
    return conn.execute(stmt).inserted_primary_key[0]

def _cleanup(conn, id):
    delete = City.delete().where(City.c.id == id)
    conn.execute(delete)

def _select_by_id(conn, id):
    query = City.select().where(City.c.id == id)
    return conn.execute(query).fetchone()

class Test(TestCase):
    def test_city_create(self):
        conn = create_db_engine().connect()

        # Utility connection kept open until test completion for cleanup, fetching etc..
        u_conn = create_db_engine().connect()

        city = { "name": "TestCity",
                 "district": "A",
                 "population": 10,
                 "countrycode": "USA" }

        id = create(conn, city)

        self.assertIsNotNone(id)

        _cleanup(u_conn, id)
        u_conn.close()

    def test_city_update(self):
        conn = create_db_engine().connect()

        u_conn = create_db_engine().connect()

        city = { "name": "TestCity",
                 "district": "A",
                 "population": 10,
                 "countrycode": "USA" }

        data = { "name": "UpdatedCity",
                 "district": "B" }

        id = _create(u_conn, city)

        created = _select_by_id(u_conn, id)

        update(conn, id, data)

        updated = _select_by_id(u_conn, id)

        _cleanup(u_conn, id)

        self.assertEqual(updated['name'], "UpdatedCity")
        self.assertEqual(updated['district'], "B")

        u_conn.close()
