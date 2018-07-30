from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

import os
import time

MAX_WAIT = 20

def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):

    # TODO(steve): automate with Fabric to reset the
    # database when in staging_server or else it
    # will fail without manually resetting db.
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_row_in_list_table(self, description, amount):
        rows = self.browser.find_elements_by_tag_name('td')
        self.assertIn(description, [row.text for row in rows])
        self.assertIn(description, [row.text for row in rows])