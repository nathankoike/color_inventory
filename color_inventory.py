"""
generate a color inventory of similar colors
"""

import sys
from functools import reduce
from PIL import Image

Max_Color = 255

# Sort colors by their frequency
def sort_colors(colors):
    if len(colors) < 2:
        return colors

    sorted = []

    colors1 = sort_colors(colors[0: len(colors) // 2])
    colors2 = sort_colors(colors[len(colors) // 2:])

    while colors1 and colors2:
        if (colors1[0][1] > colors2[0][1]):
            sorted.append(colors1[0])
            colors1 = colors1[1:]
        else:
            sorted.append(colors2[0])
            colors2 = colors2[1:]

    sorted += colors1
    sorted += colors2

    return sorted

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
    return avg_diff < threshold and max(diffs) < threshold

def main():
    fname = sys.argv[1].split('.')

    im = Image.open('.'.join(fname))
    pix = im.load()

    # Set the similarity threshold
    threshold = float(sys.argv[2]) if (len(sys.argv) > 2) else 0.5

    # Set the step
    step = int(sys.argv[3]) if (len(sys.argv) > 3) else 2

    colors = []

    # Get all the "unique" colors in the image
    for y in range(im.size[1]):
        # Skip every other row
        if not (y % step):
            # Completion status
            print(str((y / im.size[1]) * 100) + "%")

            for x in range(im.size[0]):
                # Skip every other column
                if not (x % step):
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

    # Quadruple the occurrences of each color to make up for skipped pixels
    for i in range(len(colors)):
        colors[i] = [colors[i][0], colors[i][1] * (step ** 2)]

    # Sort the colors by frequency
    colors = sort_colors(colors)

    # Generate a new image with the relative amounts of the colors
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            pix[x, y] = colors[0][0]
            colors[0] = [colors[0][0], colors[0][1] - 1]

            if colors[0][1] < 1:
                colors = colors[1:]

    # Save the new image
    im.save(fname[0] + "_output." + fname[-1])

    print("Done!")

if __name__ == "__main__":
    main()
