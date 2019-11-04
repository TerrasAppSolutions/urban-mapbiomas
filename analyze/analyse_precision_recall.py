import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np
from plotnine import *
from plotnine.animation import PlotnineAnimation
from plotnine.data import *
from mizani.breaks import date_breaks
from mizani.formatters import date_format

import warnings

warnings.filterwarnings("ignore")


def format_raw_data(data):
    """
    Format the data from csv to facilitate 
    accuracy calculation ex:

    fn   fp  tn     tp   year   .geo
    140  62  30898  349  1985   NaN
    133  61  30894  360  1986   NaN
    130  48  30901  369  1987   NaN

                ||
                \/

    date        category  quantity
    1985-01-01  tp        349
    1985-01-01  fn        140
    1985-01-01  fp        62
    """

    data_transp = {"date": [], "category": [], "quantity": []}

    for year in range(1985, 2018):
        fn = list(data.loc[data["year"] == year]["fn"].values)[0]
        fp = list(data.loc[data["year"] == year]["fp"].values)[0]
        tn = list(data.loc[data["year"] == year]["tn"].values)[0]
        tp = list(data.loc[data["year"] == year]["tp"].values)[0]

        data_transp["date"].append(str(year) + "-01-01")
        data_transp["category"].append("tp")
        data_transp["quantity"].append(tp)

        data_transp["date"].append(str(year) + "-01-01")
        data_transp["category"].append("fn")
        data_transp["quantity"].append(fn)

        data_transp["date"].append(str(year) + "-01-01")
        data_transp["category"].append("fp")
        data_transp["quantity"].append(fp)

        data_transp["date"].append(str(year) + "-01-01")
        data_transp["category"].append("tn")
        data_transp["quantity"].append(tn)

    return pd.DataFrame.from_dict(data_transp)


def custom_date_format1(breaks):
    """
    Function to format the date
    """
    return [x.year if x.year % 5 == 0 or x.year == 2018 else "" for x in breaks]


def chart_time_series(data):

    data = data.copy()

    category_list = data["category"].value_counts().index.tolist()
    category_cat = CategoricalDtype(categories=category_list, ordered=True)

    data["category_cat"] = data["category"].astype(str).astype(category_cat)

    p1 = (
        ggplot(data)
        + geom_bar(
            aes(x="date", y="quantity", fill="category_cat"),
            stat="identity",
            position=position_dodge(),
        )
        + scale_x_datetime(breaks=date_breaks("1 years"), labels=custom_date_format1)
        + labs(y="sample size", x="years", title="LAPIG")
        + guides(fill=guide_legend(title="Legend",))  # new
    )

    return p1 + theme(
        panel_background=element_rect(fill="gray", alpha=0.2),
        dpi=120,
        figure_size=(12, 6),  # inches
        aspect_ratio=0.3,  # height:width
    )


def get_perfomance(data_matrix):
    tp = data_matrix["tp"]
    fn = data_matrix["fn"]
    fp = data_matrix["fp"]
    tn = data_matrix["tn"]
    tnr = tn / (tn + fp)
    performance = data_matrix[["year"]]
    performance["date"] = performance["year"].astype(str) + "-01-01"
    performance["recall"] = tp / (tp + fn)
    performance["precision"] = tp / (tp + fp)
    performance["accuracy"] = (tp + tn) / (tp + tn + fp + fn)
    performance["bal_accuracy"] = (performance["recall"] + tnr) / 2
    del performance["year"]

    return performance


def performance_graph(performance_data, data_name="recall", y_label="Recall"):
    p = (
        ggplot(performance_data)
        + aes("date", data_name)
        + scale_x_datetime(
            breaks=date_breaks("1 years"),
            # date_breaks=("5 years"),
            # date_minor_breaks=("1 years"),
            # limits=["1985-01-01 T 00:00 UTC", "2018-01-01 T 00:00 UTC"],
            labels=custom_date_format1,
        )
        + ylab(y_label)
        + xlab("Year")
        + geom_line(color="blue", group=1)
        + ylim(0, 1)
        + theme_gray(base_size=14)
    )

    p = p + theme(
        axis_line=element_line(size=0.7, color="gray"),
        panel_background=element_rect(fill="gray", alpha=0.2),
        dpi=120,
        figure_size=(8, 6),
        aspect_ratio=0.2,
    )

    return p


if __name__ == "__main__":
    data = pd.read_csv("./errormatrix_infra_lapig_1anoee_export.csv")
    print(data.head())
    data = transform_data_transp(data)
    print(data.head())
