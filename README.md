## PhotoGrokfff - Tool to Wrangle Your Digitized Photographs

A Python GUI app named "PhotoGrokfff" using tkinter and PIL for photo management. 

Features:
- Load images from a folder (JPG/PNG/JPEG), ignoring hidden files.
- Display thumbnails (max 300px, aspect-preserving) in a fixed-height (350px) black container.
- Buttons: 
  - "2", "3", "4" duplicate the current image (e.g., `.copy1.jpeg`), auto-advance after 1 sec if "AutoAdvance" checked (default on).
  - "Desc" toggles a 2-line, 50-wide text box (black bg, white text) for notes, saved to `descriptions.yaml`.
  - "DeDup" deletes `.copy` files, "DeSplit" deletes `.SPLIT` files for the current original.
  - "Grid4", "Grid3", "Grid3Down", "Grid3Across", "Grid2Down", "Grid2Across" toggle red grid overlays (2x2, 3-in-2x2, 3 vertical, 3 horizontal, 2 vertical, 2 horizontal) on the thumbnail.
  - "Split4", "Split3", "Split3Down", "Split3Across", "Split2Down", "Split2Across" crop the source image into 4, 3 (skip bottom-right), 3 vertical, 3 horizontal, 2 vertical, 2 horizontal files (e.g., `.SPLIT1.jpeg`).
- Navigation: "Prev", "Next", "Prev w/ Copy", "Next w/ Copy", "Prev w/ Split", "Next w/ Split", "Goto" (entry field).
- Labels: "Image X of Y", "Total files: Z", "Copy count: N", "Split count: M" (green when >0).
- "About" button for a splash with app info.
- Argparse for input folder.


Designed by @DuttonΦ w/ coding assistant Grok (xAI March 2025)


## Setup

```python
$ pip install pillow tkinter pyyaml
```

## Run

```bash
$  python photogrokfff.py /path/to/images
```