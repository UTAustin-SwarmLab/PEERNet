"""Wraps existing inference classes with timing capabilities.

There are two componenets involved in running an inference model with
benchmarking capabilities:

1. The first is an inference class, which follows the Inference protocol
and has preprocess, infer, postprocess methods. This class effectively implements
an ML model or any computation

2. The second is an augmented version of the first class, which is wrapped
with timing and benchmarking capabilities. We implement a class decorator that
augments existing inference objects with a callback() method. Classes with a
callback method allow us to bind a callback function to be called every time a
network receives a message. We refer to classes with a callback function as
inference engines, and they are used in PEERNet's CLI for offloaded inference. We
implement enginize(), a method that turns either classes or objects passed in into
a valid inference engine.
"""

import importlib
import sys
from typing import Union, Type

from peernet.networks import Message
from peernet.metrics import MetricLogger
from peernet.metrics import Timer, Timing


from peernet.inference import (
    DummyModel,
    TorchvisionPretrainedClassifier,
    Inference,
)

# logger setup
import logging
from peernet.utils import ch

logger = logging.getLogger("enginize")
logger.setLevel(logging.WARNING)
logger.addHandler(ch)


def enginize(
    model_class: Union[Type[Inference], Inference],
) -> Union[Type[Inference], Inference]:
    """A class decorator that adds a "callback" method to model class.

    The implementation of this function is a little strange. We define a callback
    function, which calls and times the input's pipeline. We then
    monkeypatch the input, and dynamically set an attribute to include the callback
    method.

    Args:
        model_class: Union[Type[Inference], Inference] - Either a class adhering
            to the inference protocol or an instance of a class adhering to the
            inference protocol

    Returns:
        Union[Type[Inference], Inference] - Returns the input class augmented
            with a callback function
    """

    def callback(self, msg: Message):
        """The callback function to add into the model_class class/object."""
        # End the upload-time logger
        iter_l: MetricLogger = msg.logger
        iter_l.end_sub("upload")

        # using timing context manager(s), time the calls to preprocess, inference, and
        # postprocess. We also check before to see if preprocess and postprocess exist.
        #  If they don't exist, we don't run and time them.
        x = msg.data
        if hasattr(self, "preprocess") and callable(getattr(self, "preprocess")):
            with Timing(iter_l, "preprocessing"):
                x = self.preprocess(x)

        with Timing(iter_l, "inference"):
            x = self.infer(x)

        if hasattr(self, "postprocess") and callable(getattr(self, "postprocess")):
            with Timing(iter_l, "postprocessing"):
                x = self.postprocess(x)

        # Pack the return message
        ret = Message(x, iter_l)

        # Before opening a timer for download and returning the object to send back,
        # We should log how many bytes the object is. BUT, since we send an open
        # logger, we log the section before measuring how large the object is,
        # then we re-start the timing on that particular node
        down_logger = iter_l.log_section("download", Timer)

        # db = sys.getsizeof(pickle.dumps(ret))
        # iter_l.log_section("download-bytes", Value).end_collection(db)

        down_logger.start_collection()

        return ret

    # Add the callback function to model_class
    # model_class.callback = callback

    # Either monkey patch or don't based on whether we want an object or a class back'
    # This is just some of the most cursed code I've ever written
    if isinstance(model_class, type):  # Check if target is a class
        logger.debug("Not monkeypatching, since a class was passed in")
        setattr(model_class, "callback", callback)
    else:  # target is an instance
        logger.debug("Monkeypatching, since an object was passed in")
        setattr(
            model_class,
            "callback",
            callback.__get__(model_class, model_class.__class__),
        )

    return model_class


def get_engine(model_name: str, device: str) -> Inference:
    """Returns an engine from the given model name and settings.

    This is mostly for internal use in implementing the CLI. I don't
    see a major reason to use this function in custom scripts.

    Args:
        model_name: str - Name of the model to load
        device: str - Cuda/CPU device

    Returns:
        Inference: An object adhering to the inference protocol.
    """
    if "::" in model_name:
        logger.debug(
            "Attempting to import and generate engine from local python script"
        )

        for path in sys.path:
            logger.debug(path)

        module_name, object_name = model_name.split("::")
        user_module = importlib.import_module(module_name)
        user_object = getattr(user_module, object_name)

        # Runtime check to make sure the user's object follows the protocol
        if not isinstance(user_object, Inference):
            logger.error(f"""Object {user_object} from module {user_module} 
                    does not satisfy the Inference Protocol.""")
            raise TypeError(f"""Object {user_object} from module {user_module} 
                    does not satisfy the Inference Protocol.""")

        return enginize(user_object)

    if model_name == "dummy":
        return enginize(DummyModel)()
    elif model_name == "efficientnet_v2_s":
        return enginize(TorchvisionPretrainedClassifier)(
            model_name="efficientnet_v2_s",
            model_weight_name="EfficientNet_V2_S_Weights",
            device=device,
        )
    elif model_name == "efficientnet_v2_m":
        return enginize(TorchvisionPretrainedClassifier)(
            model_name="efficientnet_v2_m",
            model_weight_name="EfficientNet_V2_M_Weights",
            device=device,
        )
    elif model_name == "efficientnet_v2_l":
        return enginize(TorchvisionPretrainedClassifier)(
            model_name="efficientnet_v2_l",
            model_weight_name="EfficientNet_V2_L_Weights",
            device=device,
        )
    else:
        logger.error(f"Model name {model_name} not found. Defaulting to dummy model")
        return enginize(DummyModel)()
