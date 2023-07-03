from whos_there import __version__


def test_version():
    # real version initialized in package from poetry and resolved from resources
    assert __version__ != "0.0.0"
