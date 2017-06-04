from features import get_features, get_image
from filesworker import get_dmc_image, convert_to_jpg
from matplotlib import pyplot as plt
from PIL.Image import fromarray
from PIL import Image
import numpy


file = "D:\\CanserImages\\NoduleJpg\\1.3.6.1.4.1.14519.5.2.1.6279.6001.102790687459702089070957161759.jpg"
img = get_image(file)

# img = numpy.ndarray.astype(img, 'float32')
features_list = get_features(img)
# img = fromarray(ds.pixel_array)

