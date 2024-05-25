"""Tests behavior of /sensors/random_string.py."""
from peernet.sensors import RandomString

def test_random_string():
    """Ensures RandomString().sample() returns a corrrect length string."""
    sensor = RandomString()

    for i in range(20):
        sample = sensor.sample(size = i)
        print(f"[INFO] generated random string of length {i}: {sample}")
        assert len(sample) == i