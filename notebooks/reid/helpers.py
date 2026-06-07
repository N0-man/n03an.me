from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import AutoImageProcessor, AutoModel
from torchvision import transforms


import textwrap

import matplotlib.pyplot as plt
import math

from PIL import Image, ImageOps

def add_colored_border(img, color="green", border=10):
    return ImageOps.expand(img, border=border, fill=color)


def show_image_to_image_results(query_index, results, figsize_per_image=3.2):
    q_path = query_meta.iloc[query_index]["path"]
    q_vid = query_meta.iloc[query_index]["vid"]
    q_camid = query_meta.iloc[query_index]["camid"]

    n = len(results)
    cols = n + 1   # query/probe + all retrieved results
    rows = 1

    plt.figure(figsize=(cols * figsize_per_image, rows * figsize_per_image))

    # Query / probe image
    img = Image.open(q_path).convert("RGB")
    ax = plt.subplot(rows, cols, 1)
    ax.imshow(img)
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title(
        f"QUERY / PROBE\nvid={q_vid} cam={q_camid}",
        fontsize=14,
        fontweight="bold",
        color="white",
        backgroundcolor="blue",
        pad=8,
    )

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(4)
        spine.set_edgecolor("blue")

    # Retrieved results
    for i, row in results.iterrows():
        img = Image.open(row["path"]).convert("RGB")

        ax = plt.subplot(rows, cols, i + 2)
        ax.imshow(img)
        ax.set_xticks([])
        ax.set_yticks([])

        is_correct = bool(row["is_correct_vid"])
        is_distractor = int(row["camid"]) == -1

        border_color = "green" if is_correct else "red"

        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(4)
            spine.set_edgecolor(border_color)

        title = (
            f"R{int(row['rank'])}\n"
            f"score={row['score']:.3f}\n"
            f"vid={row['vid']} cam={row['camid']}\n"
            f"correct={row['is_correct_vid']}"
        )

        ax.set_title(
            title,
            fontsize=9,
            fontweight="bold" if is_correct else "normal",
            color=border_color,
            pad=8,
        )

        if is_distractor:
            ax.text(
                0.5,
                0.04,
                "cam=-1",
                transform=ax.transAxes,
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color="white",
                backgroundcolor="red",
            )

    plt.tight_layout()
    plt.show()


def show_queries_for_labeling(query_ids, figsize_per_image=3.2):
    if isinstance(query_ids, str):
        query_ids = [query_ids]

    n_queries = len(query_ids)
    top_k = 5

    fig, axes = plt.subplots(
        n_queries,
        top_k,
        figsize=(top_k * figsize_per_image, n_queries * figsize_per_image),
    )

    if n_queries == 1:
        axes = np.expand_dims(axes, axis=0)

    for row_idx, query_id in enumerate(query_ids):
        rows = review_results_labeled[
            review_results_labeled["query_id"] == query_id
        ].sort_values("rank").copy()

        if rows.empty:
            continue

        query = rows.iloc[0]["query"]
        wrapped_query = textwrap.fill(f"{query_id}: {query}", width=32)

        # Display actual query as row title
        axes[row_idx, 0].text(
            -0.35,
            0.5,
            wrapped_query,
            transform=axes[row_idx, 0].transAxes,
            fontsize=12,
            fontweight="bold",
            va="center",
            ha="right",
        )

        for col_idx, (_, row) in enumerate(rows.iterrows()):
            ax = axes[row_idx, col_idx]

            img = Image.open(row["path"]).convert("RGB")
            ax.imshow(img)
            ax.axis("off")

            ax.set_title(
                f"R{int(row['rank'])}\n"
                f"score={row['cosine_score']:.3f}\n"
                f"z={row['z_score']:.2f}\n"
                f"label={row['human_label']}",
                fontsize=9,
            )

    plt.tight_layout(rect=[0.12, 0, 1, 1])
    plt.show()


def show_search_results(results, title=None, cols=5, figsize_per_image=3.5):
    n = len(results)
    rows = int(np.ceil(n / cols))

    plt.figure(figsize=(cols * figsize_per_image, rows * figsize_per_image))

    if title:
        plt.suptitle(title, fontsize=14)

    for i, row in results.iterrows():
        img = Image.open(row["path"]).convert("RGB")

        plt.subplot(rows, cols, i + 1)
        plt.imshow(img)
        plt.axis("off")

        label = (
            f"R{int(row['rank'])}\n"
            f"score={row['cosine_score']:.3f}\n"
            f"z={row['z_score']:.2f}\n"
            f"vid={row['vid']} cam={row['camid']}"
        )

        plt.title(label, fontsize=9)

    plt.tight_layout()
    plt.show()