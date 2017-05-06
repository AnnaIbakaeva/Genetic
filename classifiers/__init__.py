# -*- coding: utf-8 -*-
import numpy as np
import cv2
import math
import collections
import itertools

import os

# Color spaces
CS_BGR = 101
CS_HSV = 102
CS_LUV = 103

# Color space ranges used in OpenCV. Each upper boundary is exclusive.
CS_RANGE = {
    CS_BGR: ([0, 256], [0, 256], [0, 256]),
    CS_HSV: ([0, 180], [0, 256], [0, 256]),
    CS_LUV: ([0, 256], [0, 256], [0, 256])
}


def moments_get_center(m):
    """Returns the center of mass from moments.

    1. Simon Xinmeng Liao. Image analysis by moments. (1993).
    """
    return np.array( (int(m['m10']/m['m00']), int(m['m01']/m['m00'])) )


def moments_get_skew(m):
    """Returns the skew from moments."""
    return m['mu11']/m['mu02']


def color_histograms(img, histsize=None, mask=None, colorspace=CS_BGR):
    """Convenience wrapper for :cv2:`calcHist`.

    Returns the histogram for each channel in `img`.

    The input image colorspace must be set with `colorspace`. Value can be
    one of the following:
        * ``CS_BGR`` for the BGR color space (default).
        * ``CS_HSV`` for the HSV color space.
        * ``CS_LUV`` for the CIE 1976 (L\*, u\*, v\*) color space.
    """
    if colorspace not in CS_RANGE:
        raise ValueError("Unknown colorspace %s." % colorspace)
    if histsize and len(histsize) != len(CS_RANGE[colorspace]):
        raise ValueError( "Expected 'histsize' to be of length %d, found %d" % (len(CS_RANGE[colorspace]), len(histsize)) )
    if img.ndim != len(CS_RANGE[colorspace]):
        raise ValueError("Image has %d dimensions, expected %d" %(img.ndim, len(CS_RANGE[colorspace])))

    hists = []
    for ch in range(img.ndim):
        if histsize == None:
            bins = abs(CS_RANGE[colorspace][ch][1] - CS_RANGE[colorspace][ch][0])
        else:
            bins = histsize[ch]

        ranges = CS_RANGE[colorspace][ch]
        hist = cv2.calcHist([img], [ch], mask, [bins], ranges)
        hists.append(hist)

    return hists


def color_bgr_means(src, contour, bins=20):
    """Returns the histograms for BGR images along X and Y axis.

    The contour `contour` provides the region of interest in the image `src`.
    This ROI is divided into `bins` equal sections, both horizontally and
    vertically. For each horizontal and vertical section the mean B, G, and R
    are computed and returned as a 2-tuple (hor_means, ver_means). Each mean is
    in the range 0 to 255.

    If pixels outside the contour must be ignored, then `src` should be a
    masked image (i.e. pixels outside the ROI are black).
    """
    if len(src.shape) != 3:
        raise ValueError("Input image `src` must be in the BGR color space")
    if bins < 2:
        raise ValueError("Minimum value for `bins` is 2")

    props = contour_properties([contour], 'BoundingRect')
    rect_x, rect_y, width, height = props[0]['BoundingRect']
    centroid = (width/2+rect_x, height/2+rect_y)
    longest = max([width, height])
    incr =  float(longest) / bins

    # Calculate X and Y starting points.
    x_start = centroid[0] - (longest / 2)
    y_start = centroid[1] - (longest / 2)

    # Compute the mean BGR values.
    means = [[], []]
    for i in range(bins):
        x = (incr * i) + x_start
        y = (incr * i) + y_start

        x_incr = x + incr
        y_incr = y + incr
        x_end = x_start + longest
        y_end = y_start + longest

        # Remove negative values, which otherwise result in reverse indexing.
        if x_start < 0: x_start = 0
        if y_start < 0: y_start = 0
        if x < 0: x = 0
        if y < 0: y = 0
        if x_incr < 0: x_incr = 0
        if y_incr < 0: y_incr = 0
        if x_end < 0: x_end = 0
        if y_end < 0: y_end = 0

        # Convert back to integers.
        y = int(y)
        y_start = int(y_start)
        y_incr = int(y_incr)
        y_end = int(y_end)
        x = int(x)
        x_start = int(x_start)
        x_incr = int(x_incr)
        x_end = int(x_end)

        # Select horizontal and vertical sections from the image.
        sample_hor = src[y:y_incr, x_start:x_end]
        sample_ver = src[y_start:y_end, x:x_incr]

        # Compute the mean B, G, and R for the sections.
        for i, sample in enumerate([sample_hor, sample_ver]):
            channels = cv2.split(sample)

            if len(channels) == 0:
                means[i].extend([0,0,0])
                continue

            for k in range(3):
                means[i].append( np.mean(channels[k]) )

    assert len(means[0] + means[1]) == 2 * 3 * bins, \
        "Return value length mismatch"

    return (np.uint16(means[0]), np.uint16(means[1]))


def get_largest_contour(img, mode, method):
    """Get the largest contour from a binary image.

    It is a simple wrapper for :meth:`cv2.findContours` to which `mode` and
    `method` are passed. Returns None if no contours are found.
    """
    if len(img.shape) != 2:
        raise ValueError("Input image must be binary")

    contours, hierarchy = cv2.findContours(img, mode, method)
    if len(contours) == 1:
        return contours[0]

    largest = None
    area_max = 0
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour, oriented=False)
        if area > area_max:
            area_max = area
            largest = contour
    return largest


def contour_properties(contours, properties='basic'):
    """Measure properties of contours.

    `contours` is a list of contours, or an array of contours as returned by
    :meth:`cv2.findContours`. `properties` can be a comma-separated list of
    strings, a list containing strings, the single string 'all', or the string
    'basic'. If `properties` is the string 'all', all the shape measurements
    are computed. If `properties` is not specified or if it is the string
    'basic', only 'Area', 'Centroid', and 'BoundingBox' are computed. You can
    calculate the following properties:

    * ``Area``: The number of pixels in the contour.
    * ``BoundingBox``: The smallest rectangle containing the contour.
    * ``Centroid``: The center mass of the contour. This is computed by
      fitting an ellipse.
    * ``ConvexArea``: The number of pixels in the convex hull.
    * ``ConvexHull``: The smalles convex polygon that can contain the contour.
    * ``Eccentricity``: Scalar that specifies the eccentricity of the ellipse
      that fits (in a least-squares sense) the contour. The eccentricity is the
      ratio of the distance between the center and either focus of the ellipse
      and its major axis length. The value is between 0 and 1.
    * ``Ellipse``: The ellipse that fits (in a least-squares sense) the
      contour. The ellipse is returned in the format (Centroid,
      (MinorAxisLength, MajorAxisLength), Orientation). The ellipse can only
      be computed if the contour consists of at least 5 points.
    * ``EquivDiameter``: Scalar that specifies the diameter of a circle with
      the same area as the contour. Computed as sqrt(4*Area/pi).
    * ``Extent``: Scalar that specifies the ratio of the contour area to the
      bounding box area.
    * ``Extrema``: 4-by-2 matrix that specifies the extrema points in the
      contour. Each row of the matrix contains the x- and y-coordinates of one
      of the points. The format of the vector is [top right bottom left].
    * ``MinorAxisLength``: Scalar specifying the length (in pixels) of the
      minor axis of the ellipse.
    * ``MajorAxisLength``: Scalar specifying the length (in pixels) of the
      major axis of the ellipse
    * ``Orientation``: Scalar specifying the angle (in degrees ranging from 0
      to 179 degrees) between the y-axis and the major axis of the ellipse in
      clockwise direction.
    * ``Perimeter``: Scalar specifying the distance around the boundary of the
      contour.
    * ``Solidity``: Scalar specifying the proportion of the pixels in the
      convex hull that are also in the region. Computed as Area/ConvexArea.

    If a property could not be calculated, its value will be None.

    See also: http://www.mathworks.com/help/images/ref/regionprops.html
    """
    if len(contours) == 0:
        raise ValueError("List of contours not set")
    known_names = ('Area', 'BoundingBox', 'BoundingRect', 'Centroid',
        'ConvexArea', 'ConvexHull', 'Eccentricity', 'Ellipse',
        'EquivDiameter', 'Extent', 'Extrema', 'MinorAxisLength',
        'MajorAxisLength', 'Orientation', 'Perimeter', 'Solidity')
    if isinstance(properties, str):
        if properties == 'basic':
            properties = ('Area', 'Centroid', 'BoundingBox')
        elif properties == 'all':
            properties = known_names
        else:
            properties = properties.split(',')
    if len(properties) == 0:
        raise ValueError("List of properties not set")
    for p in properties:
        if not p in known_names:
            raise ValueError("Unknown property '%s'" % p)

    stats = []
    for cnt in contours:
        # Call cv2.fitEllipse if needed.
        match = ('Centroid', 'Eccentricity', 'Ellipse', 'MinorAxisLength',
        'MajorAxisLength', 'Orientation')
        if any(p in match for p in properties):
            if len(cnt) >= 5:
                ellipse = cv2.fitEllipse(cnt)
                centroid, (b, a), angle = ellipse
                x,y = centroid
                centroid = (int(x), int(y))
            else:
                ellipse = centroid = b = a = angle = None

        # Call cv2.convexHull if needed.
        match = ('ConvexHull', 'ConvexArea', 'Solidity')
        if any(p in match for p in properties):
            hull = cv2.convexHull(cnt)

        # Call cv2.contourArea if needed.
        match = ('Area', 'EquivDiameter', 'Extent')
        if any(p in match for p in properties):
            area = cv2.contourArea(cnt)
            if not area > 0:
                continue

        # Call cv2.minAreaRect if needed.
        match = ('BoundingBox', 'Extent')
        if any(p in match for p in properties):
            min_area_rect = cv2.minAreaRect(cnt)

        props = {}
        for name in properties:
            val = None
            if name == 'Area':
                val = area
            elif name == 'BoundingBox':
                val = min_area_rect
            elif name == 'BoundingRect':
                val = cv2.boundingRect(cnt)
            elif name == 'Centroid':
                val = centroid
            elif name == 'ConvexArea':
                val = cv2.contourArea(hull)
            elif name == 'ConvexHull':
                val = hull
            elif name == 'Eccentricity':
                if ellipse == None:
                    val = None
                else:
                    f = math.sqrt(math.pow(a, 2) - math.pow(b, 2))
                    val = float(f) / a
            elif name == 'Ellipse':
                val = ellipse
            elif name == 'EquivDiameter':
                val = math.sqrt(4 * area / math.pi)
            elif name == 'Extent':
                (x,y), (w,h), _ = min_area_rect
                rect_area = w * h
                val = float(area) / rect_area
            elif name == 'Extrema':
                topmost     = tuple(cnt[cnt[:,:,1].argmin()][0])
                bottommost  = tuple(cnt[cnt[:,:,1].argmax()][0])
                leftmost    = tuple(cnt[cnt[:,:,0].argmin()][0])
                rightmost   = tuple(cnt[cnt[:,:,0].argmax()][0])
                val = (topmost, rightmost, bottommost, leftmost)
            elif name == 'MinorAxisLength':
                val = b
            elif name == 'MajorAxisLength':
                val = a
            elif name == 'Orientation':
                val = angle
            elif name == 'Perimeter':
                val = cv2.arcLength(cnt, closed=True)
            elif name == 'Solidity':
                val = float(area) / cv2.contourArea(hull)

            props[name] = val
        stats.append(props)
    return stats


def shape_outline(contour, k=10):
    """Returns a shape outline feature from a contour.

    The contour shape is measured on `k` points on both X and Y axis, with
    equal distance between each point.

    Returns a `k` by 2 array. The first column represents the outline along
    the horizontal axis, and the second column the outline along the
    vertical axis. Each tuple in a column contains the minimum and maximum
    value for the shape along that axis.

    `k` must be at least 3, and no more than the contour's bounding box
    width or height.

    Returns None when the function fails to get the outline.
    """
    im_x, im_y, im_w, im_h = cv2.boundingRect(contour)
    if k < 3 or k > im_w or k > im_h:
        raise ValueError("Illegal value for `k`")

    pointset = contour[:,0]
    outline = ([], [])
    step_x = float(im_w) / (k - 1)
    step_y = float(im_h) / (k - 1)
    for i in range(k):
        # Set the X and Y value for this position.
        y = int(im_y + (step_y * i))
        if y == im_y + im_h:
            y -= 1
        x = int(im_x + (step_x * i))
        if x == im_x + im_w:
            x -= 1

        # Get the X values for row Y.
        idx = np.where(pointset[:,1] == y)
        values = pointset[:,0][idx]
        # Save the extreme values.
        outline[0].append( (min(values) - im_x, max(values) - im_x) )

        # Get the Y values for column X.
        idx = np.where(pointset[:,0] == x)
        values = pointset[:,1][idx]
        # Save the extreme values.
        outline[1].append( (min(values) - im_y, max(values) - im_y) )

    assert len(outline[0]) == k, "Number of shape elements (%d) doesn't" \
        "match the value for k (%d)" % (len(outline[0]), k)
    assert len(outline[1]) == k, "Number of shape elements (%d) doesn't" \
        "match the value for k (%d)" % (len(outline[1]), k)

    return zip(*outline)


def deskew(img, dsize, mask=None):
    """Moment-based image deskew.

    Returns deskewed copy of source image `img`. If binary mask `mask` is
    provided, the skew is derived from the mask, otherwise the source image
    `img` is used, which in that case must be single-channel, 8-bit or a
    floating-point 2D array. Size of output image is set with (x,y) tuple
    `dsize`.

    Source: OpenCV examples
    """
    if mask != None:
        m = cv2.moments(mask, binaryImage=True)
    else:
        m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = moments_get_skew(m)
    affine_matrix = np.float32([[1, skew, -0.5*dsize[0]*skew], [0, 1, 0]])
    img = cv2.warpAffine(img, affine_matrix, dsize, flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LINEAR)
    return img


def get_major_defects(contour):
    """Returns the convexity defects of a contour sorted by severity."""
    # Get convex hull and defects.
    hull = cv2.convexHull(contour, returnPoints = False)
    defects = cv2.convexityDefects(contour, hull)

    # Get the defects and sort them decreasingly.
    major_defects = []
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        distance = d/256.0
        farthest_point = tuple(contour[f][0])
        major_defects.append( (distance, farthest_point) )
    return sorted(major_defects, reverse=True)


def naik_murthy_linear(img):
    """Hue-preserving color image enhancement.

    Provides a hue preserving linear transformation with maximum possible
    contrast. [1]

    1. Naik, S. K. & Murthy, C. A. Hue-preserving color image enhancement
       without gamut problem. IEEE Trans. Image Process. 12, 1591–8 (2003).
    """
    if img.ndim != 3:
        raise ValueError("Expected a BGR image")

    y = img / 255.0
    maxval = np.amax(y, (1,0))
    minval = np.amin(y, (1,0))
    itemset = y.itemset
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            x = y[i,j]
            for k in range(3):
                a1 = 1.0 / maxval[k]
                b1 = minval[k] * -1.0
                yn = a1 * (x[k] + b1)
                itemset((i,j,k), yn)
    y *= 255
    return np.uint8(y)


def naik_murthy_nonlinear(img, f, *args, **kwargs):
    """Hue-preserving color image enhancement.

    Provides nonlinear hue preserving transformation without gamut problem,
    provided that linear transformation is initially applied on each of the
    pixels. [1]

    Image source `img` must be in the BGR color space. Argument `f` can be
    any enhancement function for which the first argument is the pixel
    intensity, followed by optional arguments `args` or keyword arguments
    `kwargs`. If keyword argument `fmap` is set to True, `f` must be a 2d
    ``numpy.ndarray`` with the same shape as `img`. In this case, `f` is
    used as a lookup table for pixel intensities after enhancement.

    1. Naik, S. K. & Murthy, C. A. Hue-preserving color image enhancement
       without gamut problem. IEEE Trans. Image Process. 12, 1591–8 (2003).
    """
    fmap = kwargs.get('fmap')
    if fmap:
        if not isinstance(f, np.ndarray) or f.shape != img.shape[:2]:
            raise ValueError("Invalid array format for `f`")

    y = img / 255.0
    itemset = y.itemset
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            x = y[i,j]
            l = x.sum()

            assert 0 <= l <= 3, "Pixel values must be in the range 0..255"

            # Leave black pixels as is (work around zero division error).
            if l == 0:
                continue

            # Apply the enhancement function.
            if not fmap:
                fl = f(l, *args, **kwargs)
            else:
                fl = f.item((i,j))

            # Enhancing the color levels linearly.
            alpha = float(fl) / l
            if alpha <= 1:
                y[i,j] *= alpha
            else:
                # Transform the BGR color vector to CMY.
                x = 1.0 - x

                # Set new scaling factor which is <= 1.
                alpha = (3 - fl) / (3 - l)
                assert alpha <= 1, "Scaling factor must be <= 1, found %s" % alpha

                # Scale vector by factor `alpha`.
                x *= alpha

                # Transform back to BGR space.
                y[i,j] = 1.0 - x

    y *= 255
    return np.uint8(y)


def s_type_enhancement(x, delta1=0, delta2=1, m=0.5, n=2):
    """S-type enhancement function.

    This implements the S-type enhancement function for contrast
    enhancement of grey scale images. [1]

    1. Naik, S. K. & Murthy, C. A. Hue-preserving color image enhancement
       without gamut problem. IEEE Trans. Image Process. 12, 1591–8 (2003).
    """
    if delta1 <= x <= m:
        y = delta1 + (m - delta1) * math.pow((x - delta1) / (m - delta1), n)
    elif m <= x <= delta2:
        y = delta2 - (delta2 - m) * math.pow((delta2 - x) / (delta2 - m), n)
    else:
        raise ValueError("Illegal value for `x` (%s <= x <= %s)" % (delta1, delta2))
    assert delta1 <= y <= delta2, \
        "Expected `y` to be in range %s..%s, found %s" % (delta1, delta2, y)
    return y


def surf_features(img, ht=400, mask=None):
    """Exctract image features with SURF algorithm of OpenCV.

    The function takes an image in grayscale, a Hessian Threshold
    and a mask. Keypoints and descriptors are computed and returned.
    """
    surf = cv2.xfeatures2d.SURF_create(ht)
    kp, des = surf.detectAndCompute(img, mask)
    return kp, des


def get_image(name):
    base_dir = os.path.dirname(__file__)
    print(base_dir)
    im_path = os.path.join("C:\\Users\\Anna\\Pictures", name)
    img = cv2.imread(im_path)
    if str(img) == None or img.size == 0:
        raise SystemError("Failed to read %s" % im_path)
    # cv2.imshow('image', img)
    return img



img = get_image("1.jpg")
print("img.size ", img.size)
# cv2.waitKey(0)
hists = color_histograms(img)
kp, des = surf_features(img)
print("kp", kp)
print("des ", des)
