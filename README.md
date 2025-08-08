# Project: Canvas Drawer & Mower Simulator

## Overview

This project consists of two main scripts: `canvas_drawer.py` and `mower_sim.py`. The purpose of these scripts is to provide an interactive drawing tool using Pygame and a simulated mowing application. The application allows users to draw paths and simulate a lawnmower following those paths.

## Functionality

### Canvas Drawer (`canvas_drawer.py`)

- **Window Setup**: Initializes a Pygame window of a specified size (1000x1000 by default) with a background image.

- **Drawing Grid**: Provides a 10x10 grid overlay on the window to guide path drawing.

- **Interactive Drawing**: Users can draw paths using mouse clicks. Paths are grouped and can represent different mowing depths.

- **Depth Adjustment**: Users can input a depth value (1-100) to affect how paths appear. Depth influences the color of the paths.

- **Undo Functionality**: Allows users to undo the last drawn point or group of points with a keyboard shortcut.

- **Save Functionality**: Saves drawn paths and their associated depth data alongside timestamps in a JSON file. This data can be used later in simulations.

### Mower Simulator (`mower_sim.py`)

- **Loading Path Data**: Loads saved path data from a JSON file produced by the Canvas Drawer.

- **Simulating Mowing**: The script simulates a lawnmower following and "mowing" along the drawn paths. The paths are rendered with depth-adjusted green colors.

- **Animation and Movement**: The mower's movement is animated with smooth transitions. It pauses at each path point to simulate mowing.

- **Colors Adjustment**: Adjusts the path color based on the specified depth, creating a visual representation of different mowing intensities.

- **User Interaction**: While the simulation runs, users can exit the application by closing the window.

## Usage Instructions

1. **Canvas Drawer**:

   - Run `canvas_drawer.py`.
   - Click and drag to draw paths on the grid.
   - Press space to finalize a group of points.
   - Press 'Ctrl+Z' to undo the last action.
   - Press 'Ctrl+S' to save the current paths to a file.
   - Use 'Ctrl+W' to change the current drawing depth.

2. **Mower Simulator**:
   - Ensure a JSON file containing path data exists.
   - Update `DOT_DATA` in `mower_sim.py` with the desired file name.
   - Run `mower_sim.py` to simulate the mowing process.

This brief guide provides an overview of the functionalities and how to engage with each script. For detailed usage and configuration, refer to the comments and structured code in the scripts.
