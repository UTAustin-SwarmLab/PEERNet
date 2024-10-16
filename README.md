## PEERNet

PEERNet is an end-to-end profiling tool for networked robotic systems. You can read about PEERNet in our [IROS 2024 Paper](https://arxiv.org/pdf/2409.06078).

### Overview

PEERNet is a Python package enabling end-to-end real-time benchmarking of arbitrary networked robotic systems. PEERNet can be used as a Command Line Interface (CLI) or through the Python package API.

The core organization of PEERNet splits arbitrary networked and cloud robotic systems into sensors, networks, devices, and ML inference. PEERNet contains utilities for benchmarking each of these in conjunction.

### Installation
PEERNet can be installed from source like any Python package:

```sh
python -m pip install .
```

See ```pyproject.toml``` for available installation options.


### Using PEERNet

#### Using the Command Line Interface

PEERNet comes with a Command Line Interface (CLI) enabling rapid prototyping of benchmarks over default network implementations. The CLI, titled `peernet_cli` is installed along with the Python package.

At a high level, when designing a benchmark with the CLI, the user has control over a few important characteristics of a networked robotic system:

1. **Sensors**: The user specifies what type of sensor to use on an edge device. Most commonly, "sensors" will be pieces of code implemented by the user (see *Custom Sensors*).

2. **Networks**: When using the CLI, the user has the option to select between already implemented network types. See `peernet.networks` for full code of all implemented networks. Generally speaking, the user has a TCP and UDP option here.

3. **Inference**: The user specifies what Machine Learning workload will run in the cloud. For common vision workloads, we support by default the ability to use any Torchvision pretrained model without writing a single line of code. To use custom models, see *Custom ML Models* below.

You can see all the available options when running a benchmark through the CLI using `>>> peernet_cli --help` in your shell.

##### Custom sensors

In PEERNet, a *sensor* is anything you can draw a sample from. This is a powerful abstraction that enables users to compose practically any sensing modality into a PEERNet benchmark.

In code, a sensor is any Python class adhering to the sensor protocol `peernet.sensors.Sensor`.

To pass a custom sensor as an argument on the command line, you must follow these steps:

1. Implement your custom sensor as a Python class adhering to `peernet.sensors.Sensor`. For example, suppose we implement `MyCustomSensor` in `custom_sensor.py`.
2. Create an instance of your sensor in the same file as the sensor is implemented. For example, in `custom_sensor.py`, we may create 
```python
my_custom_sensor = MyCustomSensor(*args, **kwargs)
```
3. In the CLI, pass the sensor object through text using the `sensor_file::sensor_object` notation. In this case, we can pass the argument `--sensor-object custom_sensor::my_custom_sensor`.

##### Custom ML Models

Custom Machine Learning models work very similarly to custom sensors. In PEERNet, a *model* is anything that can "infer". In code-speak, a PEERNet model is a class that adheres to the `peernet.inference.Inference` protocol.

Passing custom implementations of ML models is extremely similar to passing custom implementations of sensors, where we use the `file_name::model_name` convention on the command line.

Passing custom sensors and ML models through the command line is a powerful feature that enables users to take advantage of PEERNet's implementation of networking and abstraction of the profiling process, while retaining control over specific sensing modalities and ML workloads.

##### Example: Network Throughput Estimation using Custom Sensors

Imagine a user wants to estimate the upload and download latency of a particular connection between an edge device and a server, using PEERNet. In one command on the edge device and one command on the server, we can estimate one-way delay for a network uploading strings of random length.

**Client-side Command:**
```sh
peernet_cli --client --name <name> --network zmq-tcp --network-config net_config.yaml --sensor-type external --sensor-object RandomString::cs --iterations 10000
```

**Server-side Command:**
```sh
peernet_cli --server --name <name> --network zmq-tcp --network-config net_config.yaml --model_name custom_model::custom_object --iterations 10000
```

#### Fine-grained Control with the Python API

When profiling complex, pre-existing codebases that cannot easily be fit into the CLI framework, we interact directly with PEERNet modules to add end-to-end profiling capability to the codebase.

Here, we go through each of the functional modules of PEERNet and explain how they are used to benchmark custom codebases.

1. **Sensors:** In PEERNet, sensors are anything you can sample from. These include traditional sensors like cameras and lidar scanners as well as datasets (sampling an image). PEERNet provides this basic abstraction of a sensor through the protocol `peernet.sensors.Sensor`. When using PEERNet to profile custom code-bases, it is not essential to adhere to the sensor protocol, but the abstraction can be useful in many situtaions.

2. **Networks:** In PEERNet, networks connect edge and cloud devices. PEERNet provides a few implementations of common networking protocols such as ZMQ and TCP (Implemented through PyZMQ). In PEERNet's abstraction, networks importantly implement `send()` and `recv()` methods. The exact implementation takes different forms depending on the networking pattern. Furthermore, by interacting with the `metrics` module, we implement `send_with_timing()` and `recv_with_timing()`. See any of the pre-implemented networks in `peernet.networks` for reference.

3. **Inference**: In PEERNet, models are anythign that can *infer*. This is a powerful abstraction that encapsulates not only machine learning models such as deep neural networks, but practically any computation that can be done on an edge device or in the cloud. We implement `peernet.inference.Inference` to aid in constructing inference modules with good levels of abstraction, but, as was the case with sensors, adhering to these protocols is only essential when using the CLI.

    **Inference Engines**: PEERNet has a concept of an "inference engine," or a wrapper around a model that introduces automatic profiling capabilities. Implemented in `peernet.inference.enginize.py`, the `enginize()` function allows users to automatically decorate models with profiling capabilities.

4. **Metrics**: The core functionality of PEERNet allowing for one-way delay estimation and profiling through the above levls of abstraction is the `peernet.metrics` module. see `docs/metrics/` for detailed information on using the `peernet.metrics` module.