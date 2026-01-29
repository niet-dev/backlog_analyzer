from data import backlog, mappings

import pandas as pd


def main():
    export_data = pd.read_csv("data.csv")
    backlog_data = backlog.BacklogExport(
        export_data, mappings.INFINITE_BACKLOG_MAPPING)
    backlog_data.generate()

    print(backlog_data.get_dataframe())


if __name__ == "__main__":
    main()
