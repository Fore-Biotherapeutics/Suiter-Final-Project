import numpy as np
import cv2
import tf_pose_estimation.my_tf_pose_estimation as tfpose
import image_background_remove_tool.my_background_removal as background_removal
import my_math
import PySimpleGUI as sg
from PIL import Image
import os

def hex2BGR(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))[::-1]

def change_suit_color(suit_img, trousers_color, shirt_color, jacket_color):
    from skimage import data, color, io, img_as_float
    import blend_modes

    trousers_mask = cv2.imread("images/suit/trousers_mask.png", cv2.IMREAD_GRAYSCALE)
    _, trousers_mask = cv2.threshold(trousers_mask, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    shirt_mask = cv2.imread("images/suit/shirt_mask.png", cv2.IMREAD_GRAYSCALE)
    _, shirt_mask = cv2.threshold(shirt_mask, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    jacket_mask = cv2.imread("images/suit/jacket_mask.png", cv2.IMREAD_GRAYSCALE)
    _, jacket_mask = cv2.threshold(jacket_mask, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    alpha = 0.7

    # Construct a colour image to superimpose
    color_mask = np.zeros((suit_img.shape[0], suit_img.shape[1], 3), dtype="uint8")
    color_mask[np.where(trousers_mask == 255)] = trousers_color
    color_mask[np.where(shirt_mask == 255)] = shirt_color
    color_mask[np.where(jacket_mask == 255)] = jacket_color

    # Convert the input image and color mask to Hue Saturation Value (HSV)
    # colorspace
    img_hsv = cv2.cvtColor(suit_img, cv2.COLOR_BGR2HSV)
    color_mask_hsv = cv2.cvtColor(color_mask, cv2.COLOR_BGR2HSV)

    # Replace the hue and saturation of the original image
    # with that of the color mask
    img_hsv[..., 0] = color_mask_hsv[..., 0]
    img_hsv[..., 1] = color_mask_hsv[..., 1]
    img_hsv[..., 2] = color_mask_hsv[..., 2] * alpha + img_hsv[..., 2] * (1 - alpha)

    img_masked = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    return img_masked


def get_control_points(humans, img, outline_list, outline_image):
    for part_index in humans[0].body_parts:
        body_point = [int(humans[0].body_parts[part_index].y * img.shape[0]),
                      int(humans[0].body_parts[part_index].x * img.shape[1])]

    # Put useful pose estimation points into variables
    neck_point = [int(humans[0].body_parts[1].y * img.shape[0]),
                  int(humans[0].body_parts[1].x * img.shape[1])]
    left_shoulder_point = [int(humans[0].body_parts[2].y * img.shape[0] * 1.2),
                           int(humans[0].body_parts[2].x * img.shape[1])]
    right_shoulder_point = [int(humans[0].body_parts[5].y * img.shape[0] * 1.2),
                            int(humans[0].body_parts[5].x * img.shape[1])]
    left_hip_point = [int(humans[0].body_parts[8].y * img.shape[0]),
                      int(humans[0].body_parts[8].x * img.shape[1])]
    right_hip_point = [int(humans[0].body_parts[11].y * img.shape[0]),
                       int(humans[0].body_parts[11].x * img.shape[1])]
    mid_hip_point = [int(left_hip_point[0] * 0.5 + right_hip_point[0] * 0.5),
                     int(left_hip_point[1] * 0.5 + right_hip_point[1] * 0.5)]
    left_hand_point = [int(humans[0].body_parts[4].y * img.shape[0]),
                       int(humans[0].body_parts[4].x * img.shape[1])]
    right_hand_point = [int(humans[0].body_parts[7].y * img.shape[0]),
                        int(humans[0].body_parts[7].x * img.shape[1])]
    left_arm_point = [int(humans[0].body_parts[3].y * img.shape[0]),
                      int(humans[0].body_parts[3].x * img.shape[1])]
    right_arm_point = [int(humans[0].body_parts[6].y * img.shape[0]),
                       int(humans[0].body_parts[6].x * img.shape[1])]
    left_knee_point = [int(humans[0].body_parts[9].y * img.shape[0]),
                       int(humans[0].body_parts[9].x * img.shape[1])]
    right_knee_point = [int(humans[0].body_parts[12].y * img.shape[0]),
                        int(humans[0].body_parts[12].x * img.shape[1])]
    left_foot_point = [int(humans[0].body_parts[10].y * img.shape[0]),
                       int(humans[0].body_parts[10].x * img.shape[1])]
    right_foot_point = [int(humans[0].body_parts[13].y * img.shape[0]),
                        int(humans[0].body_parts[13].x * img.shape[1])]

    # Get some control points using the pose estimation points
    radius = 100
    left_armpit_point = my_math.closest_in_circle_sector(outline_image, outline_list, left_shoulder_point, 45, 135,
                                                         radius)
    right_armpit_point = my_math.closest_in_circle_sector(outline_image, outline_list, right_shoulder_point, 45, 135,
                                                          radius)
    crotch_point = my_math.closest_in_circle_sector(outline_image, outline_list, mid_hip_point, 45, 135, radius)
    left_crotch_point = [int(crotch_point[0]), int(left_knee_point[1])]
    right_crotch_point = [int(crotch_point[0]), int(right_knee_point[1])]

    throat_point = [humans[0].body_parts[1].y * img.shape[0], humans[0].body_parts[1].x * img.shape[1]]
    torso_mid_point = [int(0.5 * (throat_point[0] + crotch_point[0])),
                       int(0.5 * (throat_point[1] + crotch_point[1]))]

    # Get arm and leg angles which will be used to find the rest of the control points
    left_arm_line_angle = np.rad2deg(np.arctan(((left_shoulder_point[0] - left_arm_point[0]) /
                                                (left_shoulder_point[1] - left_arm_point[1] + 0.0001)))) + 180
    right_arm_line_angle = np.rad2deg(np.arctan(((right_shoulder_point[0] - right_arm_point[0]) /
                                                 (right_shoulder_point[1] - right_arm_point[1] + 0.0001))))
    left_forearm_line_angle = np.rad2deg(np.arctan(((left_arm_point[0] - left_hand_point[0]) /
                                                    (left_arm_point[1] - left_hand_point[1] + 0.0001)))) + 180
    right_forearm_line_angle = np.rad2deg(np.arctan(((right_arm_point[0] - right_hand_point[0]) /
                                                     (right_arm_point[1] - right_hand_point[1] + 0.0001))))
    left_leg_line_angle = np.rad2deg(np.arctan(((left_hip_point[0] - left_knee_point[0]) /
                                                (left_hip_point[1] - left_knee_point[1] + 0.0001)))) + 180
    right_leg_line_angle = np.rad2deg(np.arctan(((right_hip_point[0] - right_knee_point[0]) /
                                                 (right_hip_point[1] - right_knee_point[1] + 0.0001))))
    left_foreleg_line_angle = np.rad2deg(np.arctan(((left_knee_point[0] - left_foot_point[0]) /
                                                    (left_knee_point[1] - left_foot_point[1] + 0.0001)))) + 180
    right_foreleg_line_angle = np.rad2deg(np.arctan(((right_knee_point[0] - right_foot_point[0]) /
                                                     (right_knee_point[1] - right_foot_point[1] + 0.0001)))) + 180
    # print(left_arm_line_angle, right_arm_line_angle, left_forearm_line_angle, right_forearm_line_angle, left_leg_line_angle, right_leg_line_angle,
    #       left_foreleg_line_angle, right_foreleg_line_angle)

    #
    origin_and_sec_deg_list = [[left_shoulder_point, [45, 135]], [right_shoulder_point, [45, 135]],
                               [mid_hip_point, [45, 135]],
                               [neck_point, [225, 245]], [neck_point, [295, 315]],
                               [left_hand_point, [left_forearm_line_angle + 85, left_forearm_line_angle + 95]],
                               [left_hand_point, [left_forearm_line_angle - 95, left_forearm_line_angle - 85]],
                               [left_arm_point, [left_arm_line_angle + 85, left_arm_line_angle + 95]],
                               [left_arm_point, [left_arm_line_angle - 95, left_arm_line_angle - 85]],
                               [left_armpit_point, [left_arm_line_angle + 85, left_arm_line_angle + 95]],
                               [left_armpit_point, [265, 275]],
                               [right_hand_point, [right_forearm_line_angle - 95, right_forearm_line_angle - 85]],
                               [right_hand_point, [right_forearm_line_angle + 85, right_forearm_line_angle + 95]],
                               [right_arm_point, [right_arm_line_angle - 95, right_arm_line_angle - 85]],
                               [right_arm_point, [right_arm_line_angle + 85, right_arm_line_angle + 95]],
                               [right_armpit_point, [right_arm_line_angle - 95, right_arm_line_angle - 85]],
                               [right_armpit_point, [265, 275]],
                               [left_crotch_point, [175, 185]], [right_crotch_point, [-5, 5]],
                               [mid_hip_point, [179, 181]], [mid_hip_point, [-1, 1]],
                               # [left_knee_point, [left_leg_line_angle - 95, left_leg_line_angle - 85]],
                               # [left_knee_point, [left_leg_line_angle + 85, left_leg_line_angle + 95]],
                               [left_knee_point, [175, 185]],
                               [left_knee_point, [-5, 5]],
                               # [right_knee_point, [right_leg_line_angle - 95, right_leg_line_angle - 85]],
                               # [right_knee_point, [right_leg_line_angle + 85, right_leg_line_angle + 95]],
                               [right_knee_point, [-5, 5]],
                               [right_knee_point, [175, 185]],
                               # [left_foot_point, [left_foreleg_line_angle + 85, left_foreleg_line_angle + 95]],
                               # [left_foot_point, [left_foreleg_line_angle - 95, left_foreleg_line_angle - 85]],
                               [left_foot_point, [175, 185]],
                               [left_foot_point, [-5, 5]],
                               # [right_foot_point, [right_foreleg_line_angle - 95, right_foreleg_line_angle - 85]],
                               # [right_foot_point, [right_foreleg_line_angle + 85, right_foreleg_line_angle + 95]],
                               [right_foot_point, [175, 185]],
                               [right_foot_point, [-5, 5]],
                               [torso_mid_point, [175, 185]], [torso_mid_point, [-5, 5]]]

    control_points = []

    for pair in origin_and_sec_deg_list:
        origin = pair[0]
        sec_deg = pair[1]

        sec_deg_vecs = [my_math.point_on_circle([0, 0], radius, sec_deg[0]),
                        my_math.point_on_circle([0, 0], radius, sec_deg[1])]

        inside_sector = [p for p in outline_list if
                         my_math.is_inside_sector(p, origin, sec_deg_vecs[0], sec_deg_vecs[1], radius)]

        closest_in_sector = my_math.closest_pixel(inside_sector, origin)
        control_points.append(closest_in_sector)

    control_points.append(torso_mid_point)

    return control_points

def process_image(person_img_path, suit_colors):

    # Load person image
    # person_img_path = "images/standing_dude.JPG"
    person_img = cv2.imread(person_img_path)
    person_h, person_w = person_img.shape[:2]

    # Load suit image
    suit_img_path = "images/suit/final_suit_white.png"
    suit_img = cv2.imread(suit_img_path, cv2.IMREAD_UNCHANGED)
    suit_h, suit_w = suit_img.shape[:2]

    #  Get suit mask from the alpha channel the of suit image
    suit_mask = suit_img[:, :, 3]
    _, suit_mask = cv2.threshold(suit_mask, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    suit_img = suit_img[:, :, 0:3]
    suit_img = cv2.bitwise_and(suit_img, suit_img, mask=suit_mask)

    trousers_color = hex2BGR(suit_colors[0])
    shirt_color = hex2BGR(suit_colors[1])
    jacket_color = hex2BGR(suit_colors[2])
    suit_img = change_suit_color(suit_img, trousers_color, shirt_color, jacket_color)

    # Resize person image to a desired height while keeping the aspect ratio the same
    desired_height = 600
    person_img = cv2.resize(person_img, (int(desired_height/person_h * person_w), desired_height))
    person_h, person_w = person_img.shape[:2]

    # Perform person segmentation to remove the background
    person_no_bgd = np.array(background_removal.remove_bgd(person_img_path))
    person_no_bgd = cv2.cvtColor(person_no_bgd, cv2.COLOR_BGR2RGB)
    person_no_bgd = cv2.resize(person_no_bgd, (person_img.shape[1], person_img.shape[0]))

    # Turn the no background image into a binary mask
    # indicating which pixels belong to the person
    person_mask = np.zeros(person_no_bgd.shape[:2])
    for h in range(person_h):
        for w in range(person_w):
            if np.array_equal(np.array(person_no_bgd[h,w]), np.array(person_img[h,w])):
                person_mask[h,w] = 255
    person_mask = person_mask.astype('uint8')

    # cv2.imshow("person_mask", person_mask)
    # cv2.waitKey(0)

    # Get pose estimation mask and humans object containing the individual body points
    # for the person
    person_pose_mask, person_humans = tfpose.estimate(person_img.copy(), model='cmu', points_only=True)

    suit_body_img = cv2.imread("images/suit/final_suit_white_body.png", cv2.IMREAD_UNCHANGED)
    suit_body_mask = suit_body_img[:, :, 3]
    _, suit_body_mask = cv2.threshold(suit_body_mask, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    suit_body_img = suit_body_img[:, :, 0:3]
    suit_pose_mask, suit_humans = tfpose.estimate(suit_body_img.copy(), model='cmu', points_only=True)

    # Get the outline of the person mask
    outline = my_math.mask_outline(person_mask)
    outline_list = my_math.mask_to_pixel_list(outline)
    outline = cv2.add(outline, person_pose_mask)
    outline_image = np.zeros_like(person_img)
    outline_image[:, :, 0] = outline
    outline_image[:, :, 1] = outline
    outline_image[:, :, 2] = outline

    # Get control points for the person to be used to match
    # for matching the suit image to the person
    person_control_points = get_control_points(person_humans, person_img, outline_list, outline_image)

    # Get suit mask outline
    suit_outline = my_math.mask_outline(suit_mask)
    suit_outline_list = my_math.mask_to_pixel_list(suit_outline)
    suit_outline_image = np.zeros_like(suit_img)
    suit_outline_image[:, :, 0] = suit_outline
    suit_outline_image[:, :, 1] = suit_outline
    suit_outline_image[:, :, 2] = suit_outline

    # suit_control_points = get_control_points(suit_humans, suit_img, suit_outline_list, suit_outline_image)

    # We always use the same suit image (but with different colors),
    # so we can calculate the control points ourselves once and then use them each time.
    suit_control_points = np.array([[0.281 * suit_h, 0.383 * suit_w], [0.276 * suit_h, 0.623 * suit_w],
                                   [0.49 * suit_h, 0.507 * suit_w], [0.16 * suit_h, 0.471 * suit_w],
                                   [0.161 * suit_h, 0.536 * suit_w], [0.384 * suit_h, 0.159 * suit_w],
                                   [0.404 * suit_h, 0.202 * suit_w], [0.292 * suit_h, 0.274 * suit_w],
                                   [0.327 * suit_h, 0.323 * suit_w], [0.248 * suit_h, 0.332 * suit_w],
                                   [0.193 * suit_h, 0.383 * suit_w], [0.375 * suit_h, 0.833 * suit_w],
                                   [0.399 * suit_h, 0.805 * suit_w], [0.289 * suit_h, 0.73 * suit_w],
                                   [0.326 * suit_h, 0.687 * suit_w], [0.236 * suit_h, 0.667 * suit_w],
                                   [0.191 * suit_h, 0.622 * suit_w], [0.491 * suit_h, 0.404 * suit_w],
                                   [0.493 * suit_h, 0.614 * suit_w], [0.463 * suit_h, 0.396 * suit_w],
                                   [0.464 * suit_h, 0.616 * suit_w], [0.622 * suit_h, 0.391 * suit_w],
                                   [0.622 * suit_h, 0.453 * suit_w], [0.623 * suit_h, 0.625 * suit_w],
                                   [0.626 * suit_h, 0.565 * suit_w], [0.799 * suit_h, 0.38 * suit_w],
                                   [0.796 * suit_h, 0.422 * suit_w], [0.797 * suit_h, 0.596 * suit_w],
                                   [0.798 * suit_h, 0.638 * suit_w], [0.376 * suit_h, 0.409 * suit_w],
                                   [0.376 * suit_h, 0.601 * suit_w], [0.376 * suit_h, 0.502 * suit_w]]).astype(int)


    # Draw person control points on person outline,
    # and suit control points on suit outline, for debugging
    for i in range(len(person_control_points)):
        cv2.circle(outline_image, tuple(person_control_points[i][::-1]), 1, (0, 0, 255), thickness=3, lineType=8, shift=0)
        cv2.circle(suit_outline_image, tuple(suit_control_points[i][::-1]), 1, (0, 0, 255), thickness=3, lineType=8, shift=0)

        # cv2.imshow("outline_image", outline_image)
        # cv2.imshow("suit_outline_image", suit_outline_image)
        # cv2.waitKey(0)




    # Create an object to perform triangulation on our person image
    subdiv = cv2.Subdiv2D((0, 0, person_w, person_h))

    # Create copies of person and suit images
    # To draw triangles on for debugging
    triangles_image = person_img.copy()
    triangles_image2 = suit_img.copy()

    # Insert person control points one by one into the object
    for p in person_control_points:
        subdiv.insert(tuple(p[::-1]))

    # Get the triangles subdividing the person image (where each vertex is aa control point)
    triangles = subdiv.getTriangleList()
    triangles = np.array(triangles, dtype=np.int32)
    triangle_indexes = []

    # Remember the order of control points in the generated triangles,
    # so we can use the same order when creating the suit image triangles
    for tri in triangles:
        triangle_indexes.append([person_control_points.index([tri[1], tri[0]]), person_control_points.index([tri[3], tri[2]]),
                                 person_control_points.index([tri[5], tri[4]])])

    # Create an empty image that will later store our final result
    final_img = np.zeros_like(person_img)

    for tri_indexes in triangle_indexes:
        # Using the triangles order we generated before,
        # get a triangle from person image
        tri1 = np.array(
            [person_control_points[tri_indexes[0]], person_control_points[tri_indexes[1]], person_control_points[tri_indexes[2]]])

        # Bounding box of the person image triangle
        rect1 = cv2.boundingRect(tri1)
        (y1, x1, h1, w1) = rect1

        # Crop the bounding box part from the person image
        cropped_triangle = person_img[y1:y1 + h1, x1:x1 + w1]
        # Create a mask indicating where the triangle is in the box
        cropped_triangle_mask = np.zeros((h1, w1)).astype('uint8')

        # The vertices of the triangle
        points = np.array([[tri1[0][1] - x1, tri1[0][0] - y1],
                           [tri1[1][1] - x1, tri1[1][0] - y1, ],
                           [tri1[2][1] - x1, tri1[2][0] - y1]])

        # Fill the area belonging to the triangle in the triangle mask with 1
        cv2.fillConvexPoly(cropped_triangle_mask, points, 1)

        # The cropped bounding box with the mask applied
        cropped_triangle = cv2.bitwise_and(cropped_triangle, cropped_triangle, mask=cropped_triangle_mask)

        tri2 = np.array([suit_control_points[tri_indexes[0]], suit_control_points[tri_indexes[1]],
                         suit_control_points[tri_indexes[2]]])

        # # Draw triangle on person image, for debuggging
        # cv2.line(triangles_image, (tri1[0, 1], tri1[0, 0]), (tri1[1, 1], tri1[1, 0]), (0, 0, 255), 1)
        # cv2.line(triangles_image, (tri1[1, 1], tri1[1, 0]), (tri1[2, 1], tri1[2, 0]), (0, 0, 255), 1)
        # cv2.line(triangles_image, (tri1[2, 1], tri1[2, 0]), (tri1[0, 1], tri1[0, 0]), (0, 0, 255), 1)
        #
        # # Draw triangle on suit image, for debuggging
        # cv2.line(triangles_image2, (tri2[0,1], tri2[0,0]), (tri2[1,1], tri2[1,0]), (0, 0, 255), 1)
        # cv2.line(triangles_image2, (tri2[1,1], tri2[1,0]), (tri2[2,1], tri2[2,0]), (0, 0, 255), 1)
        # cv2.line(triangles_image2, (tri2[2,1], tri2[2,0]), (tri2[0,1], tri2[0,0]), (0, 0, 255), 1)
        #
        # cv2.imshow("triangles_image", triangles_image)
        # cv2.imshow("triangles_image2", triangles_image2)
        # cv2.waitKey(0)

        # Bounding box of the suit image triangle
        rect2 = cv2.boundingRect(tri2)
        (y2, x2, h2, w2) = rect2

        # Crop the bounding box part from the suit image
        cropped_triangle2 = suit_img[y2:y2 + h2, x2:x2 + w2]
        # Create a mask indicating where the triangle is in the box
        cropped_triangle2_mask = np.zeros((h2, w2)).astype('uint8')

        # The vertices of the triangle
        points2 = np.array([[tri2[0][1] - x2, tri2[0][0] - y2],
                            [tri2[1][1] - x2, tri2[1][0] - y2, ],
                            [tri2[2][1] - x2, tri2[2][0] - y2]])

        # Fill the area belonging to the triangle in the triangle mask with 1
        cv2.fillConvexPoly(cropped_triangle2_mask, points2, 1)

        # The cropped bounding box with the mask applied
        cropped_triangle2 = cv2.bitwise_and(cropped_triangle2, cropped_triangle2, mask=cropped_triangle2_mask)

        # Turn points arrays into float values for warping
        points = np.float32(points)
        points2 = np.float32(points2)

        # Get matrix of warping from suit triangles to person triangles
        M = cv2.getAffineTransform(points2, points)

        # Warp the suit triangle to the shape of the person triangle
        warped_triangle = cv2.warpAffine(cropped_triangle2, M, (w1, h1), borderMode=cv2.BORDER_REFLECT)
        warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=cropped_triangle_mask)

        # Get the bounding box of the triangle in the final image
        triangle_area = final_img[y1:y1 + h1, x1:x1 + w1]

        # Paste the warped triangle in the pixels where the triangle mask is 1
        mask_index = np.where(cropped_triangle_mask == 1)
        list_of_coordinates = list(zip(mask_index[0], mask_index[1]))
        for cord in list_of_coordinates:
            triangle_area[cord[0], cord[1]] = warped_triangle[cord[0], cord[1]]



        # Set the bounding box area in the final img to be the resulting triangle area
        final_img[y1:y1 + h1, x1:x1 + w1] = triangle_area

    # Paste the warped suit onto the person img by
    # setting all parts of the final img that are black to be the corresponding
    # pixel from the person image
    for i in range(person_img.shape[0]):
        for j in range(person_img.shape[1]):
            if np.array_equal(final_img[i, j], [0, 0, 0]):
                final_img[i, j] = person_img[i, j]

    return final_img, person_control_points, suit_control_points

def process_same_image(person_img_path, suit_colors, person_control_points, suit_control_points):
    # Load person image
    # person_img_path = "images/standing_dude.JPG"
    person_img = cv2.imread(person_img_path)
    person_h, person_w = person_img.shape[:2]

    # Load suit image
    suit_img_path = "images/suit/final_suit_white.png"
    suit_img = cv2.imread(suit_img_path, cv2.IMREAD_UNCHANGED)
    suit_h, suit_w = suit_img.shape[:2]

    #  Get suit mask from the alpha channel the of suit image
    suit_mask = suit_img[:, :, 3]
    _, suit_mask = cv2.threshold(suit_mask, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    suit_img = suit_img[:, :, 0:3]
    suit_img = cv2.bitwise_and(suit_img, suit_img, mask=suit_mask)

    trousers_color = hex2BGR(suit_colors[0])
    shirt_color = hex2BGR(suit_colors[1])
    jacket_color = hex2BGR(suit_colors[2])
    suit_img = change_suit_color(suit_img, trousers_color, shirt_color, jacket_color)

    # Resize person image to a desired height while keeping the aspect ratio the same
    desired_height = 600
    person_img = cv2.resize(person_img, (int(desired_height / person_h * person_w), desired_height))
    person_h, person_w = person_img.shape[:2]

    # Create an object to perform triangulation on our person image
    subdiv = cv2.Subdiv2D((0, 0, person_w, person_h))

    # Create copies of person and suit images
    # To draw triangles on for debugging
    triangles_image = person_img.copy()
    triangles_image2 = suit_img.copy()

    # Insert person control points one by one into the object
    for p in person_control_points:
        subdiv.insert(tuple(p[::-1]))

    # Get the triangles subdividing the person image (where each vertex is aa control point)
    triangles = subdiv.getTriangleList()
    triangles = np.array(triangles, dtype=np.int32)
    triangle_indexes = []

    # Remember the order of control points in the generated triangles,
    # so we can use the same order when creating the suit image triangles
    for tri in triangles:
        triangle_indexes.append(
            [person_control_points.index([tri[1], tri[0]]), person_control_points.index([tri[3], tri[2]]),
             person_control_points.index([tri[5], tri[4]])])

    # Create an empty image that will later store our final result
    final_img = np.zeros_like(person_img)

    for tri_indexes in triangle_indexes:
        # Using the triangles order we generated before,
        # get a triangle from person image
        tri1 = np.array(
            [person_control_points[tri_indexes[0]], person_control_points[tri_indexes[1]],
             person_control_points[tri_indexes[2]]])

        # Bounding box of the person image triangle
        rect1 = cv2.boundingRect(tri1)
        (y1, x1, h1, w1) = rect1

        # Crop the bounding box part from the person image
        cropped_triangle = person_img[y1:y1 + h1, x1:x1 + w1]
        # Create a mask indicating where the triangle is in the box
        cropped_triangle_mask = np.zeros((h1, w1)).astype('uint8')

        # The vertices of the triangle
        points = np.array([[tri1[0][1] - x1, tri1[0][0] - y1],
                           [tri1[1][1] - x1, tri1[1][0] - y1, ],
                           [tri1[2][1] - x1, tri1[2][0] - y1]])

        # Fill the area belonging to the triangle in the triangle mask with 1
        cv2.fillConvexPoly(cropped_triangle_mask, points, 1)

        # The cropped bounding box with the mask applied
        cropped_triangle = cv2.bitwise_and(cropped_triangle, cropped_triangle, mask=cropped_triangle_mask)

        tri2 = np.array([suit_control_points[tri_indexes[0]], suit_control_points[tri_indexes[1]],
                         suit_control_points[tri_indexes[2]]])

        # # Draw triangle on person image, for debuggging
        # cv2.line(triangles_image, (tri1[0, 1], tri1[0, 0]), (tri1[1, 1], tri1[1, 0]), (0, 0, 255), 1)
        # cv2.line(triangles_image, (tri1[1, 1], tri1[1, 0]), (tri1[2, 1], tri1[2, 0]), (0, 0, 255), 1)
        # cv2.line(triangles_image, (tri1[2, 1], tri1[2, 0]), (tri1[0, 1], tri1[0, 0]), (0, 0, 255), 1)
        #
        # # Draw triangle on suit image, for debuggging
        # cv2.line(triangles_image2, (tri2[0,1], tri2[0,0]), (tri2[1,1], tri2[1,0]), (0, 0, 255), 1)
        # cv2.line(triangles_image2, (tri2[1,1], tri2[1,0]), (tri2[2,1], tri2[2,0]), (0, 0, 255), 1)
        # cv2.line(triangles_image2, (tri2[2,1], tri2[2,0]), (tri2[0,1], tri2[0,0]), (0, 0, 255), 1)
        #
        # cv2.imshow("triangles_image", triangles_image)
        # cv2.imshow("triangles_image2", triangles_image2)
        # cv2.waitKey(0)

        # Bounding box of the suit image triangle
        rect2 = cv2.boundingRect(tri2)
        (y2, x2, h2, w2) = rect2

        # Crop the bounding box part from the suit image
        cropped_triangle2 = suit_img[y2:y2 + h2, x2:x2 + w2]
        # Create a mask indicating where the triangle is in the box
        cropped_triangle2_mask = np.zeros((h2, w2)).astype('uint8')

        # The vertices of the triangle
        points2 = np.array([[tri2[0][1] - x2, tri2[0][0] - y2],
                            [tri2[1][1] - x2, tri2[1][0] - y2, ],
                            [tri2[2][1] - x2, tri2[2][0] - y2]])

        # Fill the area belonging to the triangle in the triangle mask with 1
        cv2.fillConvexPoly(cropped_triangle2_mask, points2, 1)

        # The cropped bounding box with the mask applied
        cropped_triangle2 = cv2.bitwise_and(cropped_triangle2, cropped_triangle2, mask=cropped_triangle2_mask)

        # Turn points arrays into float values for warping
        points = np.float32(points)
        points2 = np.float32(points2)

        # Get matrix of warping from suit triangles to person triangles
        M = cv2.getAffineTransform(points2, points)

        # Warp the suit triangle to the shape of the person triangle
        warped_triangle = cv2.warpAffine(cropped_triangle2, M, (w1, h1), borderMode=cv2.BORDER_REFLECT)
        warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=cropped_triangle_mask)

        # Get the bounding box of the triangle in the final image
        triangle_area = final_img[y1:y1 + h1, x1:x1 + w1]

        # Paste the warped triangle in the pixels where the triangle mask is 1
        mask_index = np.where(cropped_triangle_mask == 1)
        list_of_coordinates = list(zip(mask_index[0], mask_index[1]))
        for cord in list_of_coordinates:
            triangle_area[cord[0], cord[1]] = warped_triangle[cord[0], cord[1]]

        # Set the bounding box area in the final img to be the resulting triangle area
        final_img[y1:y1 + h1, x1:x1 + w1] = triangle_area

    # Paste the warped suit onto the person img by
    # setting all parts of the final img that are black to be the corresponding
    # pixel from the person image
    for i in range(person_img.shape[0]):
        for j in range(person_img.shape[1]):
            if np.array_equal(final_img[i, j], [0, 0, 0]):
                final_img[i, j] = person_img[i, j]

    return final_img, person_control_points, suit_control_points

def gui():
    from skimage import io

    desired_height = 600
    path = ""
    is_new_img = True

    layout = [
        [sg.Text(text="Enter image URL:"), sg.In(key='url'), sg.Button("Load URL")],
        [sg.FileBrowse("Browse for image", target='input')],
        [sg.In(key='input', visible=False, enable_events=True), sg.Image(key='img', size=(400, 600))],
        [sg.In(key='trousers_color', visible=False, enable_events=True, default_text="#000000"),
         sg.Button("", size=(2,1), key="trousers_color_button", disabled=True, button_color=("#000000", "#000000")),
         sg.ColorChooserButton("Trousers Color", target="trousers_color"),
         sg.In(key='shirt_color', visible=False, enable_events=True, default_text="#ffffff"),
         sg.Button("", size=(2, 1), key="shirt_color_button", disabled=True, button_color=("#ffffff", "#ffffff")),
         sg.ColorChooserButton("Shirt Color", target="shirt_color"),
         sg.In(key='jacket_color', visible=False, enable_events=True, default_text="#000000"),
         sg.Button("", size=(2, 1), key="jacket_color_button", disabled=True, button_color=("#000000", "#000000")),
         sg.ColorChooserButton("Jacket Color", target="jacket_color")],
        [sg.Button("Process Image")]
    ]

    # Create the window
    window = sg.Window("Suiter", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        if event == 'input':
            path = values['input']
            img = Image.open(path)
            img = img.resize((int(desired_height / img.size[1] * img.size[0]), desired_height))
            img.save("images/temp/temp.png", "png")
            window['img'].update(filename="images/temp/temp.png")
            is_new_img = True
        elif event == "Process Image":
            colors = (values['trousers_color'], values['shirt_color'], values['jacket_color'])
            if is_new_img:
                result_img, person_control_points, suit_control_points = process_image(path, colors)
            else:
                result_img, person_control_points, suit_control_points = process_same_image(path, colors, person_control_points, suit_control_points)
            result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            result_img = Image.fromarray(result_img)
            result_img.save("images/temp/temp_result.png", "png")
            window['img'].update(filename="images/temp/temp_result.png")
            is_new_img = False
        elif event == "Load URL":
            url = values['url']
            img = io.imread(url)
            img = Image.fromarray(img)
            img = img.resize((int(desired_height / img.size[1] * img.size[0]), desired_height))
            img.save("images/temp/temp.png", "png")
            path = "images/temp/temp.png"
            window['img'].update(filename="images/temp/temp.png")
            is_new_img = True
        elif event == "trousers_color":
            color = values['trousers_color']
            window['trousers_color_button'].update(button_color=("#000000", color))
        elif event == "shirt_color":
            color = values['shirt_color']
            window['shirt_color_button'].update(button_color=("#000000", color))
        elif event == "jacket_color":
            color = values['jacket_color']
            window['jacket_color_button'].update(button_color=("#000000", color))
        elif event == sg.WIN_CLOSED:
            os.remove("images/temp/temp_result.png")
            os.remove("images/temp/temp.png")
            break

    window.close()
    os.remove("images/temp/temp_result.png")
    os.remove("images/temp/temp.png")

if __name__ == '__main__':
    gui()







