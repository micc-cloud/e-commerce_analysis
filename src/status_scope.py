"""Reusable status-scope controls for Amazon sales analysis."""

import numpy as np
import pandas as pd


DELIVERED_STATUS = "Shipped - Delivered to Buyer"


def add_status_scope(frame: pd.DataFrame) -> pd.DataFrame:
    """Add descriptive status groups without changing source rows."""
    result = frame.copy()
    status = result["status"].astype("string")
    lowered = status.str.lower()
    result["status_group"] = np.select(
        [
            lowered.eq("cancelled"),
            lowered.str.contains("return", na=False),
            lowered.eq(DELIVERED_STATUS.lower()),
        ],
        ["cancelled", "return_related", "delivered_status_proxy"],
        default="other_status",
    )
    result["is_delivered_status_proxy"] = status.eq(DELIVERED_STATUS)
    result["analysis_scope"] = np.where(
        result["is_delivered_status_proxy"], "delivered_status_proxy", "reported_source"
    )
    return result


def amount_coverage(frame: pd.DataFrame, group_by: str) -> pd.DataFrame:
    """Return row count, populated amount count, and coverage by a dimension."""
    return frame.groupby(group_by, dropna=False).agg(
        rows=(group_by, "size"),
        amount_populated=("amount", lambda values: values.notna().sum()),
        amount_coverage=("amount", lambda values: values.notna().mean()),
    )
