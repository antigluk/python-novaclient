# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from novaclient.tests import utils
from novaclient.tests.v1_1 import fakes
from novaclient.v1_1 import aggregates


class AggregatesTest(utils.TestCase):
    def setUp(self):
        super(AggregatesTest, self).setUp()
        self.cs = self._get_fake_client()
        self.aggregate_type = self._get_aggregate_type()

    def _get_fake_client(self):
        return fakes.FakeClient()

    def _get_aggregate_type(self):
        return aggregates.Aggregate

    def test_list_aggregates(self):
        result = self.cs.aggregates.list()
        self.cs.assert_called('GET', '/os-aggregates')
        for aggregate in result:
            self.assertTrue(isinstance(aggregate, aggregates.Aggregate))

    def test_create_aggregate(self):
        body = {"aggregate": {"name": "test", "availability_zone": "nova1"}}
        aggregate = self.cs.aggregates.create("test", "nova1")
        self.cs.assert_called('POST', '/os-aggregates', body)
        self.assertTrue(isinstance(aggregate, aggregates.Aggregate))

    def test_get(self):
        aggregate = self.cs.aggregates.get("1")
        self.cs.assert_called('GET', '/os-aggregates/1')
        self.assertTrue(isinstance(aggregate, aggregates.Aggregate))

        aggregate2 = self.cs.aggregates.get(aggregate)
        self.cs.assert_called('GET', '/os-aggregates/1')
        self.assertTrue(isinstance(aggregate2, aggregates.Aggregate))

    def test_get_details(self):
        aggregate = self.cs.aggregates.get_details("1")
        self.cs.assert_called('GET', '/os-aggregates/1')
        self.assertTrue(isinstance(aggregate, aggregates.Aggregate))

        aggregate2 = self.cs.aggregates.get_details(aggregate)
        self.cs.assert_called('GET', '/os-aggregates/1')
        self.assertTrue(isinstance(aggregate2, aggregates.Aggregate))

    def test_update(self):
        aggregate = self.cs.aggregates.get("1")
        values = {"name": "foo"}
        body = {"aggregate": values}

        result1 = aggregate.update(values)
        self.cs.assert_called('PUT', '/os-aggregates/1', body)
        self.assertTrue(isinstance(result1, aggregates.Aggregate))

        result2 = self.cs.aggregates.update(2, values)
        self.cs.assert_called('PUT', '/os-aggregates/2', body)
        self.assertTrue(isinstance(result2, aggregates.Aggregate))

    def test_update_with_availability_zone(self):
        aggregate = self.cs.aggregates.get("1")
        values = {"name": "foo", "availability_zone": "new_zone"}
        body = {"aggregate": values}

        result3 = self.cs.aggregates.update(aggregate, values)
        self.cs.assert_called('PUT', '/os-aggregates/1', body)
        self.assertTrue(isinstance(result3, aggregates.Aggregate))

    def test_add_host(self):
        aggregate = self.cs.aggregates.get("1")
        host = "host1"
        body = {"add_host": {"host": "host1"}}

        result1 = aggregate.add_host(host)
        self.cs.assert_called('POST', '/os-aggregates/1/action', body)
        self.assertTrue(isinstance(result1, aggregates.Aggregate))

        result2 = self.cs.aggregates.add_host("2", host)
        self.cs.assert_called('POST', '/os-aggregates/2/action', body)
        self.assertTrue(isinstance(result2, aggregates.Aggregate))

        result3 = self.cs.aggregates.add_host(aggregate, host)
        self.cs.assert_called('POST', '/os-aggregates/1/action', body)
        self.assertTrue(isinstance(result3, aggregates.Aggregate))

    def test_remove_host(self):
        aggregate = self.cs.aggregates.get("1")
        host = "host1"
        body = {"remove_host": {"host": "host1"}}

        result1 = aggregate.remove_host(host)
        self.cs.assert_called('POST', '/os-aggregates/1/action', body)
        self.assertTrue(isinstance(result1, aggregates.Aggregate))

        result2 = self.cs.aggregates.remove_host("2", host)
        self.cs.assert_called('POST', '/os-aggregates/2/action', body)
        self.assertTrue(isinstance(result2, aggregates.Aggregate))

        result3 = self.cs.aggregates.remove_host(aggregate, host)
        self.cs.assert_called('POST', '/os-aggregates/1/action', body)
        self.assertTrue(isinstance(result3, aggregates.Aggregate))

    def test_set_metadata(self):
        aggregate = self.cs.aggregates.get("1")
        metadata = {"foo": "bar"}
        body = {"set_metadata": {"metadata": metadata}}

        result1 = aggregate.set_metadata(metadata)
        self.cs.assert_called('POST', '/os-aggregates/1/action', body)
        self.assertTrue(isinstance(result1, aggregates.Aggregate))

        result2 = self.cs.aggregates.set_metadata(2, metadata)
        self.cs.assert_called('POST', '/os-aggregates/2/action', body)
        self.assertTrue(isinstance(result2, aggregates.Aggregate))

        result3 = self.cs.aggregates.set_metadata(aggregate, metadata)
        self.cs.assert_called('POST', '/os-aggregates/1/action', body)
        self.assertTrue(isinstance(result3, aggregates.Aggregate))

    def test_delete_aggregate(self):
        aggregate = self.cs.aggregates.list()[0]
        aggregate.delete()
        self.cs.assert_called('DELETE', '/os-aggregates/1')

        self.cs.aggregates.delete('1')
        self.cs.assert_called('DELETE', '/os-aggregates/1')

        self.cs.aggregates.delete(aggregate)
        self.cs.assert_called('DELETE', '/os-aggregates/1')
