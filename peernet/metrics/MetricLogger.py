"""Base class for logging-- a tree like structure for logging iterative data."""

import os
import pandas as pd
import numbers
from typing import Type, Optional

# logging setup
import logging
from peernet.utils import ch

logger = logging.getLogger("MetricLogger")
logger.setLevel(logging.INFO)
logger.addHandler(ch)


class MetricLogger:
    """Organizes observances of an arbitrary metric into a tree."""

    def __init__(self, name: str, depth: int = 0) -> None:
        """Initialize a MetricLogger node. Also used for init of subnodes/trees.

        Args:
            name: str - name of the root node of the tree/subtree
            depth: int - 0 indexed, level of the tree this subtree belongs to
        """
        if "_" in name:
            logger.error(
                """Don't use underscores in logger name if you want 
                to be able to convert this logger to a csv."""
            )

        self.name = name
        self.depth = depth
        self.metric_name = "metric"

        self.children = []

        self.start_collection()
        self.end = None

        self.metric = None

    def _tic(self):
        raise NotImplementedError("Subclass must implement _tic method")

    def _toc(self):
        raise NotImplementedError("Subclass must implement _toc method")

    def start_collection(self, *args, **kwargs) -> None:
        """Restarts the logging for this node."""
        self._tic(*args, **kwargs)

    def end_collection(self, *args, **kwargs) -> None:
        """Ends the logging for this node."""
        # logger.debug(f"end_collection called with *args {args} and **kwargs {kwargs}")
        self.metric = self._toc(*args, **kwargs)

    def end_sub(self, name, *args, **kwargs) -> None:
        """Ends the node within self with given name."""
        # logger.debug(f"end_sub called with *args {args} and **kwargs {kwargs}")
        if self.name == name:
            self.end_collection(*args, **kwargs)
        else:
            for child in self.children:
                child.end_sub(name, *args, **kwargs)

    def log_section(
        self, name: str, subclass: Optional[Type["MetricLogger"]] = None
    ) -> Type["MetricLogger"]:
        """Adds a node to the tree.

        Args:
            name: string - name of the section to add
            subclass: MetricLogger - Subclass type, must be instance of MetricLogger

        Returns:
            checkpoint: MetricLogger - A valid MetricLogger node
        """
        if not subclass:
            checkpoint = self.__class__(name, depth=self.depth + 1)
        else:
            checkpoint = subclass(name, depth=self.depth + 1)

        self.children.append(checkpoint)
        return checkpoint

    def get_metric(self, name: str):
        """Get the metric for a child with name {name} in self's immediate children.

        Args:
            name: str - Name of child node to retrieve metric for

        Returns:
            metric if available, -1 otherwise
        """
        for child in self.children:
            if child.name == name:
                return child.metric

        return -1

    def __str__(self) -> str:
        """String representation of node."""
        ret_val = ""
        if not self.children:
            # ret_val = f"{self.name} - {self.val}\n"
            if self.metric:
                if isinstance(self.metric, numbers.Number):
                    ret_val = f"{self.name} --> {self.metric_name}: {self.metric:.4f}\n"
                else:
                    ret_val = f"{self.name} --> {self.metric_name}: {self.metric}\n"
            else:
                ret_val = f"{self.name} --> Not Ended\n"

        # Recursive case, parent node. Add self and then add children.
        else:
            # ret_val += f"{self.name} - {self.val}\n"
            if self.metric:
                if isinstance(self.metric, numbers.Number):
                    ret_val = f"{self.name} --> {self.metric_name}: {self.metric:.4f}\n"
                else:
                    ret_val = f"{self.name} --> {self.metric_name}: {self.metric}\n"
            else:
                ret_val = f"{self.name} --> Not Ended\n"

            for checkpoint in self.children:
                ret_val += checkpoint.depth * "    " + checkpoint.__str__()

        return ret_val

    def save_txt(self, name: str = "metric_logging", dir_name: str = "") -> None:
        """Saves the logger and all subloggers into a txt file.

        Args:
            name: str - Name of file
            dir_name: str - Name of parent directory
        """
        if dir_name:
            if dir_name[-1] != "/":
                dir_name += "/"

            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

        if ".txt" not in name:
            name += ".txt"

        text_file = open(dir_name + name, "w")
        text_file.write(self.__str__())
        text_file.close()

    def __update_depth(self, updater: int) -> None:
        """Increment depth of this node and children nodes by updater.

        Args:
            updater: int - Value to update node depth by
        """
        self.depth += updater
        for checkpoint in self.children:
            checkpoint.__update_depth(updater)

    def __propagate_depth(self) -> None:
        """Propagate this node's depth to all children."""
        for child in self.children:
            child.depth = self.depth + 1
            child.__propagate_depth()

    def __zero_depth(self) -> None:
        """Make this node a root node (by depth)."""
        self.depth = 0
        self.__propagate_depth()

    def insert(self, new: Type["MetricLogger"]):
        """Insert a child node.

        Args:
            new: MetricLogger - Node to insert
        """
        new.__zero_depth()
        new.__update_depth(self.depth + 1)
        self.children.append(new)

    def asdict(self) -> None:
        """Return a dictionary representation of this tree."""
        if not self.children:
            return {self.name: (self.metric, None)}

        else:
            child_dicts = [child.asdict() for child in self.children]
            combined = dict()
            for child_dict in child_dicts:
                for key in child_dict:
                    combined[key] = child_dict[key]

            return {self.name: (self.metric, combined)}

    def copy_from(self, other: Type["MetricLogger"]):
        """Copies all information from other into self.

        Args:
            other: MetricLogger - Root node of tree to copy from.
        """
        self.name = other.name

        # self.depth remains unchanged, since this needs to still be a valid
        # subtree in self's tree.

        self.children = other.children

        # When copying other metric logger types, they may not have
        # Start and end.
        if hasattr(other, "start"):
            self.start = other.start

        if hasattr(other, "end"):
            self.end = other.end

        self.metric = other.metric

        self.__propagate_depth()

    def to_csv(self, dest: str, index_depth: int = 1) -> pd.DataFrame:
        """Writes self to a csv using a custom intermediate representation format.

        Args:
            dest: csv file to write to
            index_depth: What depth of node to use as the index column. Default = 1.

        Returns:
            df: pd.DataFrame - Pandas dataframe representing the csv written.
        """
        d = {}

        def dfs(node, path=""):
            if node.depth < index_depth:
                if node.children:
                    for child in node.children:
                        dfs(child)
                else:
                    return

            elif node.depth == index_depth:
                # We only want to add val column if index node is not a container
                if node.metric_name != "Container":
                    if "val" not in d:
                        d["val"] = []
                    d["val"].append(node.metric)

                if node.children:
                    for child in node.children:
                        dfs(child)

                else:
                    return

            else:
                # Create a path for this node that's deeper than index_depth
                if not path:
                    p = node.name
                else:
                    p = path + "_" + node.name

                # Append value immediaately
                if not node.children:
                    if p not in d:
                        d[p] = []
                    d[p].append(node.metric)

                # Append as value
                else:
                    # Again, we never add val for containers
                    if node.metric_name != "Container":
                        p_prime = p + "_val"

                        if p_prime not in d:
                            d[p_prime] = []
                        d[p_prime].append(node.metric)

                    for child in node.children:
                        dfs(child, path=p)

        dfs(self)  # Returns nothing, but populates d

        d["iteration"] = range(len(d[[i for i in d.keys()][0]]))

        logger.debug(f"Intermediate dictionary:\n{d}")

        df = pd.DataFrame(d)
        df = df.set_index("iteration")

        # We only want to use multi-indexing if any of the column headers actually have hierarchical indexes  # noqa: E501
        if any(["_" in c for c in df.columns]):
            df.columns = pd.MultiIndex.from_tuples(
                [tuple(c.split("_")) for c in df.columns]
            )

        df.to_csv(dest, header=True)

        return df


def pd_from_csv(csvfile: str) -> pd.DataFrame:
    """Read csv intermediate representation into a pandas dataframe.

    This function should only be used for csv files that were written with
    hierarchical indexes. For csv files written without hierarchical indexing,
    use pd.read_csv directly.

    Args:
        csvfile: str - csv file to read from

    Returns:
        df: pd.DataFrame - Output pandas dataframe.
    """
    if not os.path.exists(csvfile):
        logger.critical(f"{csvfile} is not a valid path.")

    return pd.read_csv(csvfile, header=[0, 1], index_col=0)
