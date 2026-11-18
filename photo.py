# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

FILES = [
    ("temp/setup_function_completion.tsv", "Setup Function Completion", "temp/setup_function_completion.png"),
    ("temp/global_completion.tsv", "Global Completion", "temp/global_completion.png"),
    ("temp/path_completion.tsv", "Path Completion", "temp/path_completion.png"),
]


def plot_one(tsv_path: str, title: str, out_png: str) -> None:
    df = pd.read_csv(tsv_path, sep="\t")
    frameworks = df.columns[1:]

    plt.figure(figsize=(14, 8))
    for framework in frameworks:
        plt.plot(df.index + 1, df[framework], marker="o", alpha=0.8, label=framework)

    plt.title(title)
    plt.xlabel("Order")
    plt.ylabel("Value (ms)")
    plt.xticks(df.index + 1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close()


def plot_combined() -> None:
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(14, 24))

    for ax, (tsv_path, title, _) in zip(axes, FILES):
        df = pd.read_csv(tsv_path, sep="\t")
        frameworks = df.columns[1:]
        for framework in frameworks:
            ax.plot(df.index + 1, df[framework], marker="o", alpha=0.8, label=framework)

        ax.set_title(title)
        ax.set_xlabel("Order")
        ax.set_ylabel("Value (ms)")
        ax.set_xticks(df.index + 1)
        ax.grid(True, alpha=0.3)
        ax.legend()

    plt.tight_layout()
    plt.savefig("temp/combined_plots.png", dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    for tsv_path, title, out_png in FILES:
        plot_one(tsv_path, title, out_png)
    plot_combined()
    print("All individual plots and the combined plot saved successfully.")

