import os
import random
import matplotlib

from config import n_count, interval

# Try to use a GUI backend
try:
    os.environ.setdefault("QT_LOGGING_RULES", "*.debug=false;*.warning=false")
    matplotlib.use("Qt5Agg")
except Exception:
    pass

import matplotlib.pyplot as plt

# -------------------------
# Dark Mode Theme Configuration
# -------------------------
plt.style.use('dark_background')
COLORS = {
    'bg': '#0d1117',
    'bars': '#58a6ff',
    'bars_sorted': '#3fb950',
    'bars_comparing': '#f85149',
    'text': '#c9d1d9',
    'grid': '#30363d'
}


# -------------------------
# Sorting algorithms (generators with tracking)
# -------------------------
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            yield arr, [j, j + 1], []
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, [], [j, j + 1]


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            yield arr, [j, j + 1], []
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, [], [j + 1]
        arr[j + 1] = key
        yield arr, [], [j + 1]


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield arr, [j, min_idx], []
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield arr, [], [i, min_idx]


def merge_sort(arr, start=0, end=None):
    if end is None:
        end = len(arr)
    if end - start <= 1:
        return
    mid = (start + end) // 2
    yield from merge_sort(arr, start, mid)
    yield from merge_sort(arr, mid, end)
    left = arr[start:mid]
    right = arr[mid:end]
    i = j = 0
    for k in range(start, end):
        if j >= len(right) or (i < len(left) and left[i] <= right[j]):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        yield arr, [k], []


def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low >= high:
        return
    pivot = arr[high]
    i = low
    for j in range(low, high):
        yield arr, [j, high], []
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            yield arr, [], [i, j]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    yield arr, [], [i, high]
    yield from quick_sort(arr, low, i - 1)
    yield from quick_sort(arr, i + 1, high)


def heap_sort(arr):
    n = len(arr)

    def heapify(n_, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n_ and arr[l] > arr[largest]:
            largest = l
        if r < n_ and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr, [], [i, largest]
            yield from heapify(n_, largest)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr, [], [i, 0]
        yield from heapify(i, 0)


# -------------------------
# visualization
# -------------------------
def visualize_live(sort_generator_func, arr, interval_s=0.01):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    algo_name = sort_generator_func.__name__.replace("_", " ").title()
    ax.set_title(algo_name, fontsize=16, color=COLORS['text'], pad=20, fontweight='bold')

    # Create bars with gradient effect
    bars = ax.bar(range(len(arr)), arr, align="edge", width=0.8,
                  color=COLORS['bars'], edgecolor='none')

    ax.set_xlim(-0.5, len(arr))
    ax.set_ylim(0, max(arr) * 1.15)
    ax.set_xlabel('Index', color=COLORS['text'], fontsize=10)
    ax.set_ylabel('Value', color=COLORS['text'], fontsize=10)

    # Style grid
    ax.grid(True, alpha=0.2, color=COLORS['grid'], linestyle='--', linewidth=0.5)
    ax.tick_params(colors=COLORS['text'])

    # Info text boxes
    ops_text = ax.text(0.02, 0.97, "", transform=ax.transAxes,
                       fontsize=11, color=COLORS['text'],
                       verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor=COLORS['bg'],
                                 edgecolor=COLORS['grid'], alpha=0.8))

    status_text = ax.text(0.98, 0.97, "", transform=ax.transAxes,
                          fontsize=11, color=COLORS['text'],
                          verticalalignment='top', horizontalalignment='right',
                          bbox=dict(boxstyle='round', facecolor=COLORS['bg'],
                                    edgecolor=COLORS['grid'], alpha=0.8))

    plt.ion()
    plt.tight_layout()
    plt.show()

    it = 0
    comparing_count = 0
    swap_count = 0
    working_arr = arr.copy()

    # Flag to track if window is closed
    window_closed = [False]

    def on_close(event):
        window_closed[0] = True

    fig.canvas.mpl_connect('close_event', on_close)

    try:
        for state in sort_generator_func(working_arr):
            # Check if window was closed
            if window_closed[0]:
                print("\n❌ Visualization interrupted by user.")
                return

            it += 1
            new_arr, comparing, swapped = state

            if comparing:
                comparing_count += 1
            if swapped:
                swap_count += 1

            # Update bar heights and colors
            for idx, (rect, val) in enumerate(zip(bars, new_arr)):
                rect.set_height(val)

                # Color based on state
                if idx in comparing:
                    rect.set_color(COLORS['bars_comparing'])
                    rect.set_alpha(0.9)
                elif idx in swapped:
                    rect.set_color(COLORS['bars_sorted'])
                    rect.set_alpha(1.0)
                else:
                    # Gradient based on value
                    ratio = val / max(arr)
                    rect.set_color(COLORS['bars'])
                    rect.set_alpha(0.5 + 0.5 * ratio)

            # Update info
            ops_text.set_text(f"Operations: {it}\nComparisons: {comparing_count}\nSwaps: {swap_count}")
            status_text.set_text("Sorting...")

            plt.pause(interval_s)

    except Exception as e:
        print(f"Error during sorting: {e}")

    # Final state - show all bars as sorted
    plt.ioff()
    for rect, val in zip(bars, working_arr):
        rect.set_height(val)
        ratio = val / max(arr)
        rect.set_color(COLORS['bars_sorted'])
        rect.set_alpha(0.6 + 0.4 * ratio)

    ops_text.set_text(f"Operations: {it}\nComparisons: {comparing_count}\nSwaps: {swap_count}")
    status_text.set_text("✓ Complete!")
    status_text.set_color('#3fb950')

    fig.canvas.draw_idle()
    print(f"\n{'=' * 50}")
    print(f"Algorithm: {algo_name}")
    print(f"Total Operations: {it}")
    print(f"Comparisons: {comparing_count}")
    print(f"Swaps: {swap_count}")
    print(f"{'=' * 50}")
    print("\nSorting complete! Close the window when ready.")

    # Keep window open and responsive
    plt.show(block=True)


# -------------------------
# Menu
# -------------------------
if __name__ == "__main__":
    algos = {
        "1": ("Bubble Sort", bubble_sort),
        "2": ("Insertion Sort", insertion_sort),
        "3": ("Selection Sort", selection_sort),
        "4": ("Merge Sort", lambda a: merge_sort(a, 0, len(a))),
        "5": ("Quick Sort", lambda a: quick_sort(a, 0, len(a) - 1)),
        "6": ("Heap Sort", heap_sort),
    }

    print("\n" + "=" * 50)
    print("  SORTING ALGORITHM VISUALIZER (Dark Mode)")
    print("=" * 50)
    print("\nChoose an algorithm:")
    for k, v in algos.items():
        print(f"  [{k}] {v[0]}")
    print("=" * 50)

    choice = input("\nEnter your choice (1-6): ").strip()
    if choice not in algos:
        print("❌ Invalid choice. Exiting.")
        raise SystemExit

    N = n_count
    arr = list(range(1, N + 1))
    random.shuffle(arr)

    print(f"\n🚀 Starting {algos[choice][0]}...")
    print(f"Array size: {N} elements\n")

    visualize_live(algos[choice][1], arr, interval_s=interval)
