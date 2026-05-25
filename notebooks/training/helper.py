import xml.etree.ElementTree as ET
import os
import random

from pathlib import Path
from collections import defaultdict

import numpy as np
from PIL import Image
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, Sampler
import torchvision.transforms as T

import torchreid

import math
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

def parse_veri_xml(xml_path):
    with open(xml_path, "r", encoding="utf-8") as f:
        xml_data = f.read() 

    tree = ET.fromstring(xml_data)

    meta = {}

    for elem in tree.iter():
        attrs = {k.lower(): v for k, v in elem.attrib.items()}
        if not attrs:
            continue

        img_name = (attrs.get("imagename"))
        vehicleid_raw = (attrs.get("vehicleid"))
        cam_raw = (
            attrs.get("cameraid")
        )
        color_raw = attrs.get("colorid")
        type_raw = attrs.get("typeid")

        try:
            pid = int(vehicleid_raw) if vehicleid_raw is not None else -1
        except:
            continue

        if isinstance(cam_raw, str) and cam_raw.lower().startswith("c"):
            camid = int(cam_raw[1:])
        else:
            continue
            
        try:
            colorid = int(color_raw) if color_raw is not None else None
        except:
            colorid = None

        try:
            typeid = int(type_raw) if type_raw is not None else None
        except:
            typeid = None

        meta[img_name] = {
            "pid": pid,
            "camid": camid,
            "color": colorid,
            "type": typeid,
        }

    return meta

def read_name_list(txt_path):
    with open(txt_path, "r") as f:
        names = [ln.strip() for ln in f.readlines() if ln.strip()]
    return names

def parse_per_query_index_lists(index_txt_path, query_names, test_names):
    with open(index_txt_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) == len(query_names), (
        f"Line count mismatch: {index_txt_path} has {len(lines)} lines, "
        f"but query_names has {len(query_names)}"
    )

    out = {}
    n_gallery = len(test_names)

    for qname, line in zip(query_names, lines):
        if not line:
            out[qname] = set()
            continue

        # Parse 1-based ints, convert to 0-based
        idxs_1b = [int(x) for x in line.split()]
        idxs_0b = [i - 1 for i in idxs_1b]

        bad = [i for i in idxs_0b if i < 0 or i >= n_gallery]
        if bad:
            raise ValueError(
                f"Invalid gallery indices in {index_txt_path} for query {qname}: {bad[:10]}"
            )

        out[qname] = set(idxs_0b)

    return out



def show_images_grid(image_names, image_dir, title=None, cols=6, figsize_per_cell=(3.2, 3.2)):
    image_dir = Path(image_dir)
    n = len(image_names)
    if n == 0:
        print(f"{title or 'Images'}: no images to display")
        return

    rows = math.ceil(n / cols)
    fig_w = cols * figsize_per_cell[0]
    fig_h = rows * figsize_per_cell[1]

    fig, axes = plt.subplots(rows, cols, figsize=(fig_w, fig_h))
    if rows == 1:
        axes = [axes] if cols == 1 else axes
    axes = axes.flatten() if hasattr(axes, "flatten") else axes

    for ax in axes:
        ax.axis("off")

    for i, name in enumerate(image_names):
        ax = axes[i]
        img = Image.open(image_dir / name).convert("RGB")
        ax.imshow(img)
        ax.set_title(name, fontsize=8)
        ax.axis("off")

    if title:
        fig.suptitle(title, fontsize=14, y=1.02)

    plt.tight_layout()
    plt.show()

def visualize_topk_side_by_side(
    qf, qnames, gf, gnames,
    gt_idx_map, jk_idx_map,
    image_query_dir, image_test_dir,
    query_idx=0,
    topk=12,
    gallery_cols=4,
    show_junk=True,              # False = hide JK from ranked display
    fig_width=22,
    row_height=3.6,
    query_title_fontsize=14,
    item_title_fontsize=10,
    show_filenames=True,
    show_score=True,
    score_mode="similarity",     # "similarity" or "distance"
    border_width=4
):
    """
    Layout:
      [ Query (large) ] [ Gallery grid ... ]
    Tags:
      GT = green, JK = gray, NG = red

    score_mode:
      - "similarity": cosine similarity (higher is better)
      - "distance":   1 - cosine similarity (lower is better)
    """
    # Cosine similarity matrix (features are already normalized)
    simmat = torch.mm(qf, gf.t()).cpu().numpy()
    # Distance matrix for ranking (ascending)
    distmat = 1.0 - simmat

    qname = qnames[query_idx]
    gt_set = gt_idx_map.get(qname, set())
    jk_set = jk_idx_map.get(qname, set())

    ranked = np.argsort(distmat[query_idx]).tolist()
    if not show_junk:
        ranked = [gidx for gidx in ranked if gidx not in jk_set]
    ranked = ranked[:topk]

    # Grid sizing
    gallery_rows = math.ceil(len(ranked) / gallery_cols)
    total_rows = max(2, gallery_rows)
    total_cols = gallery_cols + 1

    fig_height = max(8, row_height * total_rows)
    fig = plt.figure(figsize=(fig_width, fig_height))
    border_color = "black" 
    border_width = 2       

    fig.patch.set_edgecolor(border_color)
    fig.patch.set_linewidth(border_width)
    fig.patch.set_facecolor("white") 

    width_ratios = [1.7] + [1.0] * gallery_cols
    gs = fig.add_gridspec(
        total_rows, total_cols,
        width_ratios=width_ratios,
        hspace=0.35,
        wspace=0.18
    )

    # --- Query panel ---
    axq = fig.add_subplot(gs[:, 0])
    qimg = Image.open(Path(image_query_dir) / qname).convert("RGB")
    axq.imshow(qimg)
    axq.axis("off")

    axq.set_title(
        f"QUERY (Probe)\n{qname}\nGT: {len(gt_set)} | JK: {len(jk_set)}",
        fontsize=query_title_fontsize,
        fontweight="bold",
        pad=10
    )

    for spine in axq.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(border_width)
        spine.set_edgecolor("black")

    # --- Gallery panels ---
    for i, gidx in enumerate(ranked):
        r = i // gallery_cols
        c = (i % gallery_cols) + 1
        ax = fig.add_subplot(gs[r, c])

        gname = gnames[gidx]
        gimg = Image.open(Path(image_test_dir) / gname).convert("RGB")

        if gidx in jk_set:
            tag = "Junk Image"
            color = "gray"
        elif gidx in gt_set:
            tag = "Ground Truth"
            color = "green"
        else:
            tag = "Incorrect"
            color = "red"

        sim = float(simmat[query_idx, gidx])
        dist = float(distmat[query_idx, gidx])

        ax.imshow(gimg)
        ax.axis("off")

        # Score text
        if show_score:
            if score_mode == "similarity":
                score_txt = f"sim={sim:.4f}"
            elif score_mode == "distance":
                score_txt = f"d={dist:.4f}"
            else:
                raise ValueError("score_mode must be 'similarity' or 'distance'")
        else:
            score_txt = None

        # Title
        parts = [f"R{i+1}", tag]
        if score_txt:
            parts.append(score_txt)
        line1 = " | ".join(parts)

        if show_filenames:
            title = f"{line1}\n{gname}"
        else:
            title = line1

        ax.set_title(title, fontsize=item_title_fontsize, color=color, pad=6)

        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(border_width)
            spine.set_edgecolor(color)

    # Hide unused slots
    total_slots = gallery_rows * gallery_cols
    for j in range(len(ranked), total_slots):
        r = j // gallery_cols
        c = (j % gallery_cols) + 1
        ax_empty = fig.add_subplot(gs[r, c])
        ax_empty.axis("off")

    plt.show()