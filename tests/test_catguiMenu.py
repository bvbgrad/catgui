import pytest

import catguiMenu

pytestmark = pytest.mark.skip("PySimpleGUI modules not testable?")

pytest.mark.skip
def test_get_scan_date():
    assert (len(catguiMenu.get_scan_date()) == 10, "Date string is 10 characters"