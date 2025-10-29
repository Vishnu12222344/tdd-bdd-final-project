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
Test Factory to make fake objects for testing
"""

import factory
from factory import fuzzy
from service.models import Product, Category


# pylint: disable=too-few-public-methods
class ProductFactory(factory.Factory):
    """Creates fake Products for testing"""

    class Meta:
        """Meta configuration for ProductFactory"""
        model = Product

    id = factory.Sequence(lambda n: n)
    name = fuzzy.FuzzyChoice(["Widget", "Gadget", "Doodad", "Thingamajig"])
    description = factory.Faker("sentence", nb_words=6)
    price = fuzzy.FuzzyDecimal(1.0, 100.0, 2)
    available = fuzzy.FuzzyChoice([True, False])
    category = fuzzy.FuzzyChoice(list(Category))
