# -*- coding: utf-8 -*-
# Copyright 2016 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from behave import given
from behave import then
from behave import when

from .util import call_cmd
from .util import create_consumer_group
from .util import create_random_topic
from .util import produce_example_msg

test_groups = ['group1', 'group2', 'group3']


@given('we have a set of existing consumer groups')
def step_impl1(context):
    topic = create_random_topic(1, 1)
    produce_example_msg(topic)

    for group in test_groups:
        create_consumer_group(topic, group)


def call_list_groups():
    cmd = ['kafka-consumer-manager',
           '--cluster-type', 'test',
           '--cluster-name', 'test_cluster',
           '--discovery-base-path', 'tests/acceptance/config',
           'list_groups']
    return call_cmd(cmd)


@when('we call the list_groups command')
def step_impl2(context):
    context.output = call_list_groups()


@then('the groups will be listed')
def step_impl3(context):
    for group in test_groups:
        assert group in context.output
