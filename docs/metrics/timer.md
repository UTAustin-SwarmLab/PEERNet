## Timer
```Timer``` is a subclass of ```MetricLogger``` designed to measure latency of code steps.

This document is only a functional specification of ```Timer```. For a detailed explanation of the parent class, ```MetricLogger```, see [here](metric_logger.md).

### Start/Stop
Timing is started and stoppped using the two methods:
```python
Timer.start_collection() -> None
```
and
```python
Timer.end_collection() -> float
```

```end_collection()``` can also be replaced by the following when a reference to a timer object is not maintained. Note that this syntax will end the *first* occurrence of a subsection with the given name.
```python
Timer.end_sub(subsection_name: str) -> float
```

### Sections and Subsections
Sections and subsections are added to Timer instances using 
```python
section: Timer = log_section(name: str)
```

### Context Manager
The context manager for ```Timer``` is ```Timing```.

Example:
```python
main_timer = Timer("main-timer-name")
with Timing(main_timer, "sub-timer-name"):
    do_stuff()
```