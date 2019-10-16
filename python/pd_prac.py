import pandas as pd

df = pd.DataFrame(
    [["0001", "John", "Engineer"], ["0002", "Lily", "Sales"]],
    columns=[
        "id",
        "standing ovation",
        "mean",
        "median",
        "variance",
        "standard deviation",
    ],
)

df.to_csv("employee.csv", index=False)
