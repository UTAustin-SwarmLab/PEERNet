"""Tests the intermediate representation (hierarchical index)."""

from peernet.metrics import Timer, Timing, pd_from_csv
import time


def test_get_ir():
    """Tests simple performance of retrieving csv."""
    try:
        t = Timer("root")
        t.start_collection()

        for i in range(2):
            t_sub = t.log_section(f"iteration-{i}")
            t_sub.start_collection()

            d = t_sub.log_section("down")
            d.end_collection()

            inf = t_sub.log_section("inference")
            pre = inf.log_section("pre")
            pre.end_collection()
            post = inf.log_section("post")
            post.end_collection()
            inf.end_collection()

            t_sub.end_collection()

        t.end_collection()

        print(f"\nHuman Readable:\n{t}")
        print(f"\nDictionary Rep:\n{t.asdict()}")
        print(f"\nIntermediate Rep:\n{t.to_csv('ir.csv', index_depth=1)}")

        assert True
    except Exception:
        assert False


def test_ir_simple():
    """Tests simple dictionary and csv IR."""
    try:
        t = Timer("root")

        for i in range(10):
            with Timing(t, f"{i}"):
                time.sleep(0.1)

        t.end_collection()

        print(f"\nHuman Readable:\n{t}")
        print(f"\nDictionary Rep:\n{t.asdict()}")
        print(f"\nIntermediate Rep:\n{t.to_csv('ir.csv', index_depth=1)}")

        assert True

    except Exception:
        assert False


def test_pd_to_csv():
    """Tests pandas and csv integration."""
    print("\n\n")
    try:
        # Make a timer
        t = Timer("root")
        t.start_collection()

        for i in range(2):
            t_sub = t.log_section(f"iteration-{i}")
            t_sub.start_collection()

            d = t_sub.log_section("down")
            d.end_collection()

            inf = t_sub.log_section("inference")
            pre = inf.log_section("pre")
            pre.end_collection()
            post = inf.log_section("post")
            post.end_collection()
            inf.end_collection()

            t_sub.end_collection()

        t.end_collection()

        # Save it to csv
        print(f"Intermediate rep:\n {t.to_csv('ir.csv', index_depth=1)}")

        # Read it back from csv
        print(f"\n\nRe-read rep:\n {pd_from_csv('ir.csv')}")
        assert True

    except Exception:
        assert False
