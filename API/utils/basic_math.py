import math


def cal_dist(point1, point2):
    return math.sqrt(math.pow(point2[0] - point1[0], 2) + math.pow(point2[1] - point1[1], 2))


def cal_angle(point1, point2, point3):
    a = math.sqrt(
        (point2[0] - point3[0]) * (point2[0] - point3[0]) + (point2[1] - point3[1]) * (point2[1] - point3[1]))
    b = math.sqrt(
        (point1[0] - point3[0]) * (point1[0] - point3[0]) + (point1[1] - point3[1]) * (point1[1] - point3[1]))
    c = math.sqrt(
        (point1[0] - point2[0]) * (point1[0] - point2[0]) + (point1[1] - point2[1]) * (point1[1] - point2[1]))

    B = math.degrees(math.acos((b * b - a * a - c * c) / (-2 * a * c)))

    return B


def cal_veloctiy(point1, point2, fps):
    distance = cal_dist(point1, point2)
    return distance * fps


def tlwh2xywh(box):
    return [box[0] + box[2] / 2, box[1] + box[3] / 2, box[2], box[3]]


def xywh2xyxy(box):
    return [box[0] - box[2] / 2, box[1] - box[3] / 2, box[0] + box[2] / 2, box[1] + box[3] / 2]


def fill_gaps(data_list, max_gap=3):
    gap = 0
    last_data = 0
    for idx, data in enumerate(data_list):
        if data == 0:
            gap += 1
        else:
            if 0 < gap <= max_gap:
                step = (data - last_data) / (gap + 1)
                for i in range(gap, 0, -1):
                    data_list[idx - i] = last_data + step * (gap - i + 1)
            gap = 0
            last_data = data
    return data_list


def get_IOU(box1, box2):
    box1 = xywh2xyxy(box1)
    box2 = xywh2xyxy(box2)
    left_column_max = max(box1[0], box2[0])
    right_column_min = min(box1[2], box2[2])
    up_row_max = max(box1[1], box2[1])
    down_row_min = min(box1[3], box2[3])
    if left_column_max >= right_column_min or down_row_min <= up_row_max:
        return 0
    else:
        S1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        S2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        S_cross = (down_row_min - up_row_max) * (right_column_min - left_column_max)
        return S_cross / (S1 + S2 - S_cross)


def cal_endpoint(start_point, center_point):
    end_point = []
    delta_x = start_point[0] - center_point[0]
    delta_y = start_point[1] - center_point[1]
    end_point.append(center_point[0]-delta_x)
    end_point.append(center_point[1]-delta_y)
    return end_point


def judge_side(start_point, end_point, target_point):

    return
