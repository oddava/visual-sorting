# 🎨 Sorting Algorithm Visualizer

A beautiful, real-time sorting algorithm visualizer with a modern dark theme. Watch various sorting algorithms come to life with color-coded comparisons, swaps, and detailed statistics.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **Real-time Visualization**: Watch sorting algorithms execute step-by-step
- **Detailed Statistics**: Track operations, comparisons, and swaps in real-time
- **6 Sorting Algorithms**: Bubble, Insertion, Selection, Merge, Quick, and Heap Sort

## 🚀 Demo

The visualizer displays bars representing array elements, with colors changing dynamically to show:
- Which elements are currently being compared
- When swaps occur
- The final sorted state with a beautiful green gradient

## 📋 Requirements

- Python 3.7+
- matplotlib
- numpy

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/oddava/sorting-visualizer.git
cd sorting-visualizer
```

2. Install dependencies:
```bash
uv sync
```

## 💻 Usage

Run the script:
```bash
uv run python realtime_sort_visualizer.py
```

Then select an algorithm from the menu:
```
[1] Bubble Sort
[2] Insertion Sort
[3] Selection Sort
[4] Merge Sort
[5] Quick Sort
[6] Heap Sort
```

The visualization window will open and display the sorting process in real-time. After completion, you'll see:
- Total operations performed
- Number of comparisons
- Number of swaps

Close the window when you're done viewing.

## 🎯 Supported Algorithms

| Algorithm | Time Complexity (Average) | Space Complexity |
|-----------|--------------------------|------------------|
| Bubble Sort | O(n²) | O(1) |
| Insertion Sort | O(n²) | O(1) |
| Selection Sort | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(log n) |
| Heap Sort | O(n log n) | O(1) |

## 🎨 Color Scheme

The visualizer uses a carefully chosen dark color palette:
- **Background**: `#0d1117` (GitHub dark)
- **Default Bars**: `#58a6ff` (Blue)
- **Comparing**: `#f85149` (Red)
- **Sorted/Swapped**: `#3fb950` (Green)
- **Text**: `#c9d1d9` (Light gray)
- **Grid**: `#30363d` (Dark gray)

## 🛠️ Customization

You can easily customize the visualization by modifying these parameters in the code:

config.py
```python
# Array size
n_count = 60  # Change to visualize more or fewer elements

# Animation speed
interval=0.01  # Decrease for faster, increase for slower
```

## 📝 How It Works

Each sorting algorithm is implemented as a Python generator that yields the array state after each operation. The visualizer:

1. Creates a matplotlib figure with bars representing array elements
2. Iterates through the generator, updating bar heights and colors
3. Uses `plt.pause()` for real-time animation
4. Tracks and displays statistics throughout the process
5. Shows the final sorted state with completion message

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new sorting algorithms
- Improve the visualization
- Enhance the UI/UX
- Fix bugs
- Add new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by the need to understand sorting algorithms visually
- Built with Python and Matplotlib
- Dark theme inspired by GitHub's color palette

## 📧 Contact

If you have any questions or suggestions, feel free to open an issue or submit a pull request!

---

⭐ Star this repository if you find it helpful!