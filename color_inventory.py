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

# Get all the colors in the image
def get_colors(x, y, step, threshold, img):
    colors = []

    # Get all the "unique" colors in the image
    for r in range(y):
        # Skip every other row
        if not (r % step):
            # Completion status
            print(str((r / y) * 100) + "%")

            for c in range(x):
                # Skip every other column
                if not (c % step):
                    found = False

                    # Check if we have already found a similar color
                    for i in range(len(colors)):
                        if (similar(colors[i][0], img[c, r], threshold)):
                            found = True
                            colors[i] = [colors[i][0], colors[i][1] + 1]
                            break

                    # If not, we have a unique color and we should add it
                    if not found:
                        colors.append([img[c, r], 1])

    return colors

# Generate a new image with the colors
def generate_inventory(im, pix, colors, fname):
    # Generate a new image with the relative amounts of the colors
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            pix[x, y] = colors[0][0]
            colors[0] = [colors[0][0], colors[0][1] - 1]

            if colors[0][1] < 1:
                colors = colors[1:]

    # Save the new image
    im.save(fname[0] + "_inventory." + fname[-1])

def main():
    # Open the settings file
    with open("settings.txt", "r") as file:
        fname = "" # The image file to open
        threshold = 0.5 # The similarity threshold
        step = 2 # The x and y step

        # The contents of the file
        settings = file.read().split('\n')

        # For every setting in the file
        for setting in settings:
            if (len(setting)):
                [option, value] = [e.strip() for e in setting.split('=')]

                # Set the settings
                if (option == "file" or option == "fname") and fname == "":
                    fname = value.split('.') # The split is for later
                if option == "threshold":
                    threshold = float(value)
                if option == "step":
                    step = int(value)

        # Check that we have a filename
        if not len(fname):
            print("Please provide a filename")
            return

        # Try to open the image
        try:
            im = Image.open('.'.join(fname))
        except:
            print("Please provide a valid filename")
            file.close()
            return

        # Get all the pixels in the image
        pix = im.load()

        # Get all the colors in the image
        colors = get_colors(im.size[0], im.size[1], step, threshold, pix)

        # Adjust color occurrence numbers to account for step
        for i in range(len(colors)):
            colors[i] = [colors[i][0], colors[i][1] * (step ** 2)]

        # Sort the colors by frequency
        colors = sort_colors(colors)

        # Generate a new image with the colors as an inventory
        generate_inventory(im, pix, colors, fname)

        # Print a nice finishing message
        print("Done!")

        file.close()

if __name__ == "__main__":
    main()
