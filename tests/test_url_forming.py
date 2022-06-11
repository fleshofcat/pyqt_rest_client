import pytest

from pyqt_rest_client import url


@pytest.mark.parametrize(
    "expected, url_parts, args",
    [
        (
            "http://server:1234/api/v1.8/projects/ex/?created=once&updated=now",
            ["projects", "ex"],
            {"created": "once", "updated": "now"},
        ),
        ("http://server:1234/api/v1.8/datasets/", ["datasets"], None),
    ],
)
def test_url__good_case(login_mock, expected, url_parts, args):
    assert url.url(url_parts, args) == expected


@pytest.mark.parametrize("bad_val", [[], ["", ""], ["part", ""]])
def test_url_value_error(bad_val):
    with pytest.raises(ValueError):
        url.url(bad_val)
