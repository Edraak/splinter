# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import unittest

from splinter import Browser
from base import BaseBrowserTests
from fake_webapp import EXAMPLE_APP


class ZopeTestBrowserDriverTest(BaseBrowserTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser('zope.testbrowser', wait_time=0.1)

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(self):
        self.browser.quit()

    def test_should_support_with_statement(self):
        with Browser('zope.testbrowser') as internet:
            pass

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'mockfile.txt'
        )
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').first.click()

        html = self.browser.html
        assert 'text/plain' in html
        assert open(file_path).read() in html

    def test_forward_to_none_page(self):
        "should not fail when trying to forward to none"
        browser = Browser('zope.testbrowser')
        browser.visit(EXAMPLE_APP)
        browser.forward()
        self.assertEqual(EXAMPLE_APP, browser.url)
        browser.quit()

    def test_cant_switch_to_frame(self):
        "zope.testbrowser should not be able to switch to frames"
        with self.assertRaises(NotImplementedError) as cm:
            self.browser.get_iframe('frame_123')
            self.fail()

        e = cm.exception
        self.assertEqual("zope.testbrowser doesn't support frames.", e.args[0])

    def test_simple_type(self):
        """
        zope.testbrowser won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.type('query', 'with type method')

    def test_simple_type_on_element(self):
        """
        zope.testbrowser won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name('query').type('with type method')

    def test_slowly_typing(self):
        """
        zope.testbrowser won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.type('query', 'with type method', slowly=True)

    def test_slowly_typing_on_element(self):
        """
        zope.testbrowser won't support type method
        on element because it doesn't interac with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            query = self.browser.find_by_name('query')
            query.type('with type method', slowly=True)

    def test_cant_mouseover(self):
        "zope.testbrowser should not be able to put the mouse over the element"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_css('#visible').first.mouse_over()

    def test_cant_mouseout(self):
        "zope.testbrowser should not be able to mouse out of an element"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_css('#visible').first.mouse_out()

    def test_links_with_nested_tags_xpath(self):
        links = self.browser.find_by_xpath('//a/span[text()="first bar"]/..')
        self.assertEqual(
            len(links), 1,
            'Found not exactly one link with a span with text "BAR ONE". %s' % (
                map(lambda item: item.outer_html, links)))
