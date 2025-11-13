# mypy: disable-error-code="no-any-return"


"""Capture SWAP simulation results in a `Result` object.

Classes:
    Result: Result of a model run.
"""

import re

from pandas import DataFrame
from pydantic import BaseModel, ConfigDict, Field, computed_field

__all__ = ["Result"]


class Result(BaseModel):
    """Result of a model run.

    Stores the run log, parsed outputs and warnings.

    Attributes:
        log (str): The log file of the model run.
        output (dict): Mapping of output names to their contents (e.g., 'csv', 'csv_tz', 'blc').
        warning (list[str] | None): List of warnings produced by the run.

    Methods:
        ascii: dict of non-CSV outputs.
        csv: pandas.DataFrame for the 'csv' output.
        csv_tz: pandas.DataFrame for the 'csv_tz' output (depth-varying variables).
        iteration_stats: Extracted iteration statistics section from the log.
        blc_summary: String of the .blc output if present.
        yearly_summary: Yearly sums of CSV variables as a DataFrame (raises TypeError if CSV missing).

        output (dict): The output file of the model run.
        warning (List[str]): The warnings of the model run.
    """

    log: str | None = Field(default=None, repr=False)
    output: dict | None = Field(default_factory=dict, repr=False)
    warning: list[str] | None = Field(default=None, repr=False)

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )

    @computed_field(return_type=dict, repr=False)
    def ascii(self) -> dict:
        """Return all outputs in ASCII format."""
        return {k: v for k, v in self.output.items() if not k.endswith("csv")}

    @computed_field(return_type=DataFrame, repr=False)
    def csv(self) -> DataFrame:
        """Return the output of the csv file as a pandas DataFrame."""
        return self.output.get("csv", None)

    @computed_field(return_type=DataFrame, repr=False)
    def csv_tz(self) -> DataFrame:
        """Return the output of the csv_tz file as a pandas DataFrame.

        The csv_tz file contains simulations of variables varying with depth over time.
        """
        return self.output.get("csv_tz", None)

    @computed_field(return_type=str, repr=False)
    def iteration_stats(self) -> str:
        """Print the iteration statistics from the log."""
        match = re.search(r".*(Iteration statistics\s*.*)$", self.log, re.DOTALL)
        if match:
            return match.group(1)
        return ""

    @computed_field(return_type=str, repr=False)
    def blc_summary(self) -> str:
        """Print the .blc file if it exists."""
        print(self.output.get("blc", None))
        return

    @computed_field(return_type=DataFrame, repr=False)
    def yearly_summary(self) -> DataFrame:
        """Return yearly sums of all output variables."""
        if not isinstance(self.csv, DataFrame):
            msg = "CSV file not included in output file formats."
            raise TypeError(msg)
        return self.csv.resample("YE").sum()
