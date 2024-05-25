"""Tests functionality of Timer subclass of MetricLogger."""

from peernet.metrics import Timer
import time


def test_single_node():
    """Tests a tree with a single node."""
    try:
        timer = Timer("root")
        timer.start_collection()
        time.sleep(1)
        timer.end_collection()
        print(f"The timer is \n{timer}")
        assert True

    except Exception:
        assert False


def test_with_children():
    """Tests trees with children."""
    try:
        timer = Timer("root")
        timer.start_collection()

        time.sleep(1)

        a = timer.log_section("a")
        time.sleep(1)
        b = timer.log_section("b")
        time.sleep(1)

        a.end_collection()
        b.end_collection()

        timer.end_collection()

        print(f"The timer is: \n{timer}")
        assert True

    except Exception:
        assert False


def test_dict_repr_simple():
    """Tests dictionary representation."""
    try:
        timer = Timer("root")
        timer.start_collection()
        time.sleep(1)
        timer.end_collection()

        print(f"timer as a dict: \n{timer.asdict()}")

    except Exception:
        assert False


def test_dict_repr_complex():
    """Tests a more complex variety of dictionary representation."""
    try:
        timer = Timer("root")
        timer.start_collection()

        time.sleep(1)

        a = timer.log_section("a")
        time.sleep(1)
        b = timer.log_section("b")
        time.sleep(1)

        a.end_collection()
        b.end_collection()

        timer.end_collection()

        print(f"The timer dict rep is : \n{timer.asdict()}")
        assert True

    except Exception:
        assert False


def test_insertion():
    """Tests insertion of nodes."""
    try:
        A = Timer("A")
        A.start_collection()

        B = Timer("B")
        B.start_collection()

        time.sleep(1)
        B.end_collection()

        time.sleep(1)
        A.end_collection()

        A.insert(B)

        print(A)

        assert True
    except Exception:
        assert False


def test_overhead():
    """Tests overhead in explicit starting and implicit starting of timers."""
    try:
        # Implicitly starting the timer
        A = Timer("A")
        time.sleep(1)
        A.end_collection()
        print(A)

        # Explicitly starting the timer
        B = Timer("B")
        B.start_collection()
        time.sleep(1)
        B.end_collection()
        print(B)

        assert True

    except Exception:
        assert False


def test_get_metric():
    """Tests retrieval of a metric."""
    try:
        A = Timer("A")
        time.sleep(1)
        b = A.log_section("b")
        time.sleep(1)
        b.end_collection()
        A.end_collection()

        print(f"Searched val: {A.get_metric('b')}")
        assert True
    except Exception:
        assert False
