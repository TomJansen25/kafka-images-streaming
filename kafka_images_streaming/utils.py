import matplotlib.pyplot as plt
import numpy as np


def visualize_image(image_array: np.ndarray):
    """
    Visualizes the decoded image using matplotlib.
    """
    plt.imshow(image_array)
    plt.axis("off")  # Hide axis
    plt.show()
