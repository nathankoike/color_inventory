"""
generate a color inventory of similar colors
"""

import sys
from functools import reduce
from PIL import Image

Max_Color = 255

# Determine the relative similarity of two colors
def similar(color1, color2, threshold):
    diffs = []

    # For each of RGBA
    for i in range(len(color1)):
        lst = [color1[i], color2[i]]

        # The percentage difference from the max value
        diffs.append((max(lst) - min(lst)) / Max_Color)

    # The average percentage difference from white
    avg_diff = reduce(lambda n, m: n + m, diffs) / len(diffs)

    # Determine if the average similarity is above the threshold
    return avg_diff <= threshold

def main():
    im = Image.open(sys.argv[1])
    pix = im.load()

    # Set the similarity threshold
    threshold = float(sys.argv[2]) if (len(sys.argv) > 2) else 0.5

    colors = []

    print(im.size)

    for y in range(im.size[1]):
        # Skip every other row
        if not (y % 2):
            print(y)
            print(len(colors), "\n")

            for x in range(im.size[0]):
                # Skip every other column
                if not (x % 2):
                    found = False

                    # Check if we have already found a similar color
                    for i in range(len(colors)):
                        if (similar(colors[i][0], pix[x, y], threshold)):
                            found = True
                            colors[i] = [colors[i][0], colors[i][1] + 1]
                            break

                    # If not, we have a unique color and we should add it
                    if not found:
                        colors.append([pix[x,y], 1])

    print(colors)

if __name__ == "__main__":
    main()
