#!/usr/bin/env python3
# Copyright 2013, Big Switch Networks, Inc.
#
# LoxiGen is licensed under the Eclipse Public License, version 1.0 (EPL), with
# the following special exception:
#
# LOXI Exception
#
# As a special exception to the terms of the EPL, you may distribute libraries
# generated by LoxiGen (LoxiGen Libraries) under the terms of your choice, provided
# that copyright and licensing notices generated by LoxiGen are not altered or removed
# from the LoxiGen Libraries and the notice provided below is (i) included in
# the LoxiGen Libraries, if distributed in source code form and (ii) included in any
# documentation for the LoxiGen Libraries, if distributed in binary form.
#
# Notice: "Copyright 2013, Big Switch Networks, Inc. This library was generated by the LoxiGen Compiler."
#
# You may not use this file except in compliance with the EPL or LOXI Exception. You may obtain
# a copy of the EPL at:
#
# http://www.eclipse.org/legal/epl-v10.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# EPL for the specific language governing permissions and limitations
# under the EPL.

import sys
import os
import unittest

root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
sys.path.insert(0, root_dir)

from generic_utils import *

class MyHash(object):
    def __init__(self, val):
        self.val = val

    def __hash__(self):
        return hash(self.val)

    def __str__(self):
        return "BoringConstantString"

    def __eq__(self, o ):
        return type(self) == type(o) and self.val == o.val

class GenericTest(unittest.TestCase):
    def test_memoize_simple(self):
        self.count = 0

        @memoize
        def function():
            self.count += 1
            return "Foo"

        self.assertEqual(0, self.count)
        self.assertEqual("Foo", function())
        self.assertEqual(1, self.count)
        self.assertEqual("Foo", function())
        self.assertEqual(1, self.count)

    def test_memoize_string_args(self):
        self.count = 0

        @memoize
        def function(a, b):
            self.count += 1
            return f"{a}:{b}"

        self.assertEqual(0, self.count)
        self.assertEqual("a:b", function('a', 'b'))
        self.assertEqual(1, self.count)
        self.assertEqual("ab:", function('ab', ''))
        self.assertEqual(2, self.count)
        self.assertEqual("ab:", function('ab', ''))
        self.assertEqual(2, self.count)

    def test_memoize_kw_args(self):
        self.count = 0

        @memoize
        def function(**kw):
            self.count += 1
            return ",".join("{k}={v}".format(k=k,v=v) for k,v in sorted(kw.items()))

        self.assertEqual(0, self.count)
        self.assertEqual("a=1", function(a=1))
        self.assertEqual(1, self.count)
        self.assertEqual("a=1,b=2", function(a=1, b=2))
        self.assertEqual(2, self.count)
        self.assertEqual("a=1", function(a=1))
        self.assertEqual(2, self.count)
        self.assertEqual("a=1,b=BoringConstantString", function(a=1, b=MyHash('1')))
        self.assertEqual(3, self.count)

    def test_memoize_with_hashable_object(self):
        self.count = 0

        @memoize
        def function(a):
            self.count += 1
            return a.val

        self.assertEqual(0, self.count)
        self.assertEqual("a", function(MyHash('a')))
        self.assertEqual(1, self.count)
        self.assertEqual("b", function(MyHash('b')))
        self.assertEqual(2, self.count)
        self.assertEqual("a", function(MyHash('a')))
        self.assertEqual(2, self.count)

if __name__ == '__main__':
    unittest.main()
