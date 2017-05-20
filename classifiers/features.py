# -*- coding: utf-8 -*-
import numpy as np
import cv2
import math
import collections
import itertools

from matplotlib import pyplot as plt

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


def get_centroid(m):
    x = m['mu10']/m['mu00']
    y = m['mu01']/m['mu00']
    return x, y


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
    hull = cv2.convexHull(contour, returnPoints=False)
    defects = cv2.convexityDefects(contour, hull)

    # Get the defects and sort them decreasingly.
    major_defects = []
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        distance = d/256.0
        farthest_point = tuple(contour[f][0])
        major_defects.append( (distance, farthest_point) )
    return sorted(major_defects, reverse=True)


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


def get_corner(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    # dst = cv2.dilate(dst,None)
    # img[dst>0.01*dst.max()]=[0,0,255]
    return dst


def feature_matcher(des1, des2):

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)

    return matches


def get_threshold(gray):
    img = cv2.medianBlur(gray, 5)

    ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


def filter_image(img):
    kernel = np.ones((5,5),np.float32)/25
    dst = cv2.filter2D(img,-1,kernel)
    return dst


def box_blur_image(img):
    blur = cv2.blur(img,(5,5))
    return blur


def gaussian_blur(img):
    blur = cv2.GaussianBlur(img,(5,5),0)
    return blur


def median_blur(img):
    median = cv2.medianBlur(img,5)
    return median


def bilaterial_filter(img):
    blur = cv2.bilateralFilter(img,9,75,75)
    return blur


def erode_image(img):
    """Удаляет шумы переднего фона
    """
    kernel = np.ones((15, 15), np.uint8)
    erosion = cv2.erode(img, kernel, iterations = 1)
    return erosion


def dilate_image(img):
    kernel = np.ones((5, 5),np.uint8)
    dilation = cv2.dilate(img, kernel, iterations = 1)
    return dilation


def erosion_by_dilation(img):
    kernel = np.ones((10, 10), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return opening


def laplacian_gradient(img):
    laplacian = cv2.Laplacian(img,cv2.CV_64F)
    return laplacian


def sobelx_gradient(img):
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
    return sobelx


def sobely_gradient(img):
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
    return sobely


def canny_edge_detection(img):
    edges = cv2.Canny(img, 25, 50)
    return edges


def find_contours(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_moments(contour):
    M = cv2.moments(contour)
    return M


def contour_approximation(cnt):
    epsilon = 0.1*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    return approx


def apply_clahe(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(img)
    return cl1


def numpy_furie(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    return fshift


def numpy_back_furie(fshift, img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, cols = gray.shape
    crow,ccol = rows/2 , cols/2
    fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return img_back


def foirier_transform(img):
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    return dft_shift


def fourier_back_transfrom(img, dft_shift):
    rows, cols = img.shape
    crow,ccol = rows/2 , cols/2

    # create a mask first, center square is 1, remaining all zeros
    mask = np.zeros((rows,cols,2),np.uint8)
    mask[crow-30:crow+30, ccol-30:ccol+30] = 1

    # apply mask and inverse DFT
    fshift = dft_shift*mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])
    return img_back


def fourier_and_back_transform(img):
    shift = foirier_transform(img)
    back_image = fourier_back_transfrom(img, shift)
    return back_image

# def find_circles(img):
#     circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
#                             param1=50,param2=30,minRadius=0,maxRadius=0)
#     return circles


def get_image(name):
    base_dir = os.path.dirname(__file__)
    print(base_dir)
    im_path = os.path.join("C:\\Users\\Anna\\Pictures", name)
    img = cv2.imread(im_path)
    if str(img) == None or img.size == 0:
        raise SystemError("Failed to read %s" % im_path)
    # cv2.imshow('image', img)
    return img

# print(img1.shape)
# img2 = get_image("11.jpg")
# print(img2.shape)
# print("img.size ", img.size)
# cv2.waitKey(0)
