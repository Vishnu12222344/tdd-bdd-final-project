# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model
"""

import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  PRODUCT MODEL TEST CASES
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """Runs once before the test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Runs once after the test suite"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()

    ######################################################################
    #  BASIC CREATE TEST
    ######################################################################
    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(
            name="Fedora",
            description="A red hat",
            price=12.50,
            available=True,
            category=Category.CLOTHS,
        )
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertAlmostEqual(product.price, 12.50, places=2)
        self.assertEqual(product.category, Category.CLOTHS)

    ######################################################################
    #  ADDITION TEST
    ######################################################################
    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        # Fix floating point precision issue
        self.assertAlmostEqual(Decimal(new_product.price), product.price, places=2)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    ######################################################################
    #  READ TEST
    ######################################################################
    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        found_product = Product.find(product.id)
        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertAlmostEqual(found_product.price, product.price, places=2)

    ######################################################################
    #  UPDATE TEST
    ######################################################################
    def test_update_a_product(self):
        """It should Update a Product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)

        # update description
        old_description = product.description
        product.description = "Updated description"
        product.update()
        self.assertNotEqual(product.description, old_description)

        # verify only one product and description updated
        products = Product.all()
        self.assertEqual(len(products), 1)
        updated = products[0]
        self.assertEqual(updated.id, product.id)
        self.assertEqual(updated.description, "Updated description")

    ######################################################################
    #  DELETE TEST
    ######################################################################
    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    ######################################################################
    #  LIST ALL TEST
    ######################################################################
    def test_list_all_products(self):
        """It should List all Products"""
        self.assertEqual(len(Product.all()), 0)
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        self.assertEqual(len(Product.all()), 5)

    ######################################################################
    #  FIND BY NAME TEST
    ######################################################################
    def test_find_by_name(self):
        """It should Find Products by Name"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        name = products[0].name
        count = len([p for p in products if p.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)

    ######################################################################
    #  FIND BY AVAILABILITY TEST
    ######################################################################
    def test_find_by_availability(self):
        """It should Find Products by Availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        availability = products[0].available
        count = len([p for p in products if p.available == availability])
        found = Product.find_by_availability(availability)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.available, availability)

    ######################################################################
    #  FIND BY CATEGORY TEST
    ######################################################################
    def test_find_by_category(self):
        """It should Find Products by Category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        category = products[0].category
        count = len([p for p in products if p.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.category, category)


if __name__ == "__main__":
    unittest.main()
