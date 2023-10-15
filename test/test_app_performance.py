import pytest

from app import Example


@pytest.fixture
def example():
    return Example()


# https://panel.holoviz.org/how_to/test/pytest.html
def test_example_performance(example: Example, benchmark):
    def select_location_and_compute():
        example.location = "USA"
        example.view()

    benchmark(select_location_and_compute)

    assert benchmark.stats["max"] < 0.03
