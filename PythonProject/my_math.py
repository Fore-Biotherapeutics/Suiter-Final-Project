import numpy as np


def does_pixel_have_black_neighbour(image, point):
    i, j = point
    h, w = image.shape[:2]
    for y in range(-1, 2):
        for x in range(-1, 2):
            if not (y == 0 and x == 0):
                if 0 < i + y < h and 0 < j + x < w and image[i + y, j + x] == 0:
                    return True
    return False


def mask_outline(mask):
    res_img = np.zeros_like(mask)
    h, w = mask.shape
    for i in range(h):
        for j in range(w):
            if mask[i, j] == 255 and does_pixel_have_black_neighbour(mask, (i, j)):
                res_img[i, j] = 255
    return res_img


def mask_to_pixel_list(mask):
    h, w = mask.shape[:2]
    pix_list = []
    for i in range(h):
        for j in range(w):
            if mask[i, j] == 255:
                pix_list.append([i, j])
    return pix_list

def dist(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def closest_pixel(pixel_list, origin):
    min_dist = np.inf
    closest = [-1, -1]
    for p in pixel_list:
        if dist(p, origin) < min_dist:
            min_dist = dist(p, origin)
            closest = p
    return closest


def is_clockwise(v1, v2):
    return -v1[1] * v2[0] + v1[0] * v2[1] > 0


def is_within_radius(v, radius):
    return v[0] ** 2 + v[1] ** 2 <= radius ** 2


def is_inside_sector(point, center, sec_start, sec_end, radius):
    rel_point = [point[0] - center[0], point[1] - center[1]]
    return is_clockwise(rel_point, sec_start) \
           and is_clockwise(sec_end, rel_point) \
           and is_within_radius(rel_point, radius)


def point_on_circle(center, radius, angle_deg):
    angle_rad = np.deg2rad(angle_deg)
    y = center[0] + radius * np.sin(angle_rad)
    x = center[1] + radius * np.cos(angle_rad)
    return [y, x]

def closest_in_circle_sector(img, img_list, origin, sec_start, sec_end, radius):
    sec_deg_vecs = [point_on_circle([0, 0], radius, sec_start),
                    point_on_circle([0, 0], radius, sec_end)]

    # cv2.circle(img, tuple(origin[::-1]), 1, (0, 255, 0), thickness=3, lineType=8, shift=0)

    inside_sector = [p for p in img_list if
                     is_inside_sector(p, origin, sec_deg_vecs[0], sec_deg_vecs[1], radius)]
    # for p in inside_sector:
    #     cv2.circle(img, tuple(p[::-1]), 0, (0, 0, 255), thickness=1, lineType=8, shift=0)

    closest_in_sector = closest_pixel(inside_sector, origin)
    # cv2.circle(img, tuple(closest_in_sector[::-1]), 0, (0, 255, 255), thickness=5, lineType=8,
    #            shift=0)
    return closest_in_sector