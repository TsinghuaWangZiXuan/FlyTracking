import os
import cv2 as cv
import numpy as np
from scipy.optimize import linear_sum_assignment
import matplotlib
import matplotlib.pyplot as plt
from data_analyze.utils.basic_math import cal_dist, cal_angle, get_IOU, fill_gaps

id2label = {'0': 'female', '1': 'male', '2': 'wing', '3': 'head', '4': 'head'}
MIN_IOU = 0.9
Inf = 1e+6


def get_cost(females_position, males_position, positions):
    cost_matrix = []
    for female_position in females_position:
        cost_matrix.append([cal_dist([float(female_position[0]), float(female_position[1])],
                                     [float(positions[0][0]), float(positions[0][1])]),
                            cal_dist([float(female_position[0]), float(female_position[1])],
                                     [float(positions[1][0]), float(positions[1][1])])])
    for male_position in males_position:
        cost_matrix.append([cal_dist([float(male_position[0]), float(male_position[1])],
                                     [float(positions[0][0]), float(positions[0][1])]),
                            cal_dist([float(male_position[0]), float(male_position[1])],
                                     [float(positions[1][0]), float(positions[1][1])])])

    return cost_matrix


def map_wing(female_pos, male_pos, wing_pos):
    if cal_dist(female_pos, wing_pos) <= cal_dist(male_pos, wing_pos):
        return 'female'
    else:
        return 'male'


def del_overlap(females_position, males_position):
    if len(females_position) == 1 and len(males_position) > 1:
        delete = []
        for idx, position in enumerate(males_position):
            if get_IOU(females_position[0], position) > MIN_IOU:
                delete.append(idx)
        for idx in delete:
            del males_position[idx]
            if len(males_position) == 1:
                break
        return females_position, males_position
    if len(males_position) == 1 and len(females_position) > 1:
        delete = []
        for idx, position in enumerate(females_position):
            if get_IOU(males_position[0], position) > MIN_IOU:
                delete.append(idx)
        for idx in delete:
            del females_position[idx]
            if len(females_position) == 1:
                break
        return females_position, males_position
    else:
        return females_position, males_position


def predict_body(body_list):
    head_x = []
    head_y = []
    tail_x = []
    tail_y = []
    for body in body_list:
        if body is not None:
            head_x.append(body[0][0])
            head_y.append(body[0][1])
            tail_x.append(body[1][0])
            tail_y.append(body[1][1])
        else:
            head_x.append(0)
            head_y.append(0)
            tail_x.append(0)
            tail_y.append(0)

    head_x = fill_gaps(head_x, Inf)
    head_y = fill_gaps(head_y, Inf)
    tail_x = fill_gaps(tail_x, Inf)
    tail_y = fill_gaps(tail_y, Inf)

    for idx, body in enumerate(body_list):
        if body is None:
            body_list[idx] = [[], []]
            body_list[idx][0].append(head_x[idx])
            body_list[idx][0].append(head_y[idx])
            body_list[idx][1].append(tail_x[idx])
            body_list[idx][1].append(tail_y[idx])

    return body_list

def cal_ang(gender_path, keypoint_path, fps, img_size):
    matplotlib.use('Qt5Agg')

    gender_file_list = os.listdir(gender_path)
    keypoint_file_list = os.listdir(keypoint_path)

    male_body = []  # head, tail, wing, wing
    female_body = []
    male_angle_list = []
    female_angle_list = []
    deprecated_frames = 0

    for file_name in gender_file_list:
        current_male_body = []
        current_female_body = []

        with open(gender_path + file_name, 'r') as gender_file:
            with open(keypoint_path + file_name, 'r') as keypoint_file:
                gender_info = gender_file.readlines()
                keypoint_info = keypoint_file.readlines()

                if gender_info == ['\n'] or keypoint_info == ['\n']:
                    deprecated_frames += 1
                    male_angle_list.append(max_male_angle)
                    female_angle_list.append(max_female_angle)
                    male_body.append(None)
                    female_body.append(None)
                    continue

                genders = []
                males_position = []
                females_position = []
                for i, line in enumerate(gender_info):
                    line = line.strip().split()
                    genders.append(line[0])
                    if line[0] == '0':
                        females_position.append([float(line[1]), float(line[2]), float(line[3]), float(line[4])])
                    elif line[0] == '1':
                        males_position.append([float(line[1]), float(line[2]), float(line[3]), float(line[4])])

                females_position, males_position = del_overlap(females_position, males_position)

                key_pioints = []
                heads_position = []
                tails_position = []
                wings_position = []
                for i, line in enumerate(keypoint_info):
                    line = line.strip().split()
                    key_pioints.append(line[0])
                    if line[0] == '3':
                        heads_position.append(line[1:])
                    elif line[0] == '4':
                        tails_position.append(line[1:])
                    elif line[0] == '2':
                        wings_position.append(line[1:])

                max_male_angle = 0
                max_female_angle = 0
                if genders.count('0') >= 1 and genders.count('1') >= 1:
                    if key_pioints.count('4') == 2 and key_pioints.count('3') == 2:
                        # head
                        head_cost_matirx = get_cost(females_position, males_position, heads_position)
                        # tail
                        tail_cost_matrix = get_cost(females_position, males_position, tails_position)

                        head_match = linear_sum_assignment(head_cost_matirx)
                        tail_match = linear_sum_assignment(tail_cost_matrix)

                        female_id = head_match[0][0]
                        if female_id >= len(females_position):
                            deprecated_frames += 1
                            male_angle_list.append(max_male_angle)
                            female_angle_list.append(max_female_angle)
                            male_body.append(None)
                            female_body.append(None)
                            continue
                        male_id = head_match[0][1]
                        if male_id < len(females_position):
                            deprecated_frames += 1
                            male_angle_list.append(max_male_angle)
                            female_angle_list.append(max_female_angle)
                            male_body.append(None)
                            female_body.append(None)
                            continue
                        else:
                            male_id -= len(females_position)

                        female_pos = [float(females_position[female_id][0]), float(females_position[female_id][1])]
                        male_pos = [float(males_position[male_id][0]), float(males_position[male_id][1])]

                        # male
                        male_head_idx = head_match[1][1]
                        male_tail_idx = tail_match[1][1]
                        male_head_pos = [float(heads_position[male_head_idx][0]), float(heads_position[male_head_idx][1])]
                        male_tail_pos = [float(tails_position[male_tail_idx][0]), float(tails_position[male_tail_idx][1])]
                        current_male_body.append([male_head_pos[0] * img_size[0], male_head_pos[1] * img_size[1]])
                        current_male_body.append([male_tail_pos[0] * img_size[0], male_tail_pos[1] * img_size[1]])

                        # female
                        female_head_idx = head_match[1][0]
                        female_tail_idx = tail_match[1][0]
                        female_head_pos = [float(heads_position[female_head_idx][0]),
                                           float(heads_position[female_head_idx][1])]
                        female_tail_pos = [float(tails_position[female_tail_idx][0]),
                                           float(tails_position[female_tail_idx][1])]
                        current_female_body.append([female_head_pos[0] * img_size[0], female_head_pos[1] * img_size[1]])
                        current_female_body.append([female_tail_pos[0] * img_size[0], female_tail_pos[1] * img_size[1]])

                        for wing in wings_position:
                            wing_pos = [float(wing[0]), float(wing[1])]
                            if map_wing(female_pos, male_pos, wing_pos) == 'male':
                                angle = cal_angle(male_tail_pos, male_head_pos, wing_pos)
                                if angle > 90:
                                    continue
                                current_male_body.append([wing_pos[0] * img_size[0], wing_pos[1] * img_size[1]])
                                if angle > max_male_angle:
                                    max_male_angle = angle
                            else:
                                angle = cal_angle(female_tail_pos, female_head_pos, wing_pos)
                                if angle > 90:
                                    continue
                                current_female_body.append([wing_pos[0] * img_size[0], wing_pos[1] * img_size[1]])
                                if angle > max_female_angle:
                                    max_female_angle = angle
                        male_body.append(current_male_body)
                        female_body.append(current_female_body)
                    else:
                        deprecated_frames += 1
                        male_body.append(None)
                        female_body.append(None)

        male_angle_list.append(max_male_angle)
        female_angle_list.append(max_female_angle)

    male_angle_list = fill_gaps(male_angle_list, fps)
    female_angle_list = fill_gaps(female_angle_list, fps)

    male_body = predict_body(male_body)
    female_body = predict_body(female_body)

    plt.subplot(1, 2, 1)
    plt.plot(male_angle_list, color='b', label='male_prediction')
    plt.hlines(np.mean(male_angle_list), 0, len(male_angle_list),
               label='mean_angle:{}'.format(np.mean(male_angle_list)))
    plt.legend()
    plt.title('male_angle')

    plt.subplot(1, 2, 2)
    plt.plot(female_angle_list, color='b', label='female_prediction')
    plt.hlines(np.mean(female_angle_list), 0, len(female_angle_list),
               label='mean_angle:{}'.format(np.mean(female_angle_list)))
    plt.legend()
    plt.title('female_angle')
    plt.show()

    img_path = 'detect/data/Samples/'
    file_list = os.listdir(img_path)
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 0)]

    video = cv.VideoWriter('data_analyze/angle/output/output.avi', cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps,
                           (img_size[0], img_size[1]))

    for idx, img_name in enumerate(file_list):
        file_name = img_path + img_name
        img = cv.imread(file_name)
        male = male_body[idx]
        female = female_body[idx]
        for i, pos in enumerate(male):
            if i >= 4:
                continue
            pos = [int(pos[0]), int(pos[1])]
            cv.circle(img, pos, 2, colors[i], -1)
            if i > 0:
                cv.line(img, pos, [int(male[0][0]), int(male[0][1])], colors[i], 2)
        for i, pos in enumerate(female):
            if i >= 4:
                continue
            pos = [int(pos[0]), int(pos[1])]
            cv.circle(img, pos, 2, colors[i], -1)
            if i > 0:
                cv.line(img, pos, [int(female[0][0]), int(female[0][1])], colors[i], 2)
        video.write(img)

    video.release()