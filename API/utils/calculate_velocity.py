import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from data_analyze.utils.basic_math import cal_veloctiy, tlwh2xywh
import argparse


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='data.txt')
    parser.add_argument('--male', type=str, default='1')
    parser.add_argument('--female', type=str, default='0')
    parser.add_argument('--fps', type=int, default=10)
    parser.add_argument('--maximum', type=int, default=500)
    parser.add_argument('--point', type=str, default='center')
    opt = parser.parse_args()
    return opt


def cal_vel(file, male, female, fps, maximum, point):

    with open(file, 'r') as file:
        data = file.readlines()
        id2gender = {male: 'male', female: 'female'}
        velocity = {male: [], female: []}
        last_position = {male: None, female: None}

        for line in data:
            line = line.strip().split()[:6]
            frame = line[0]
            gender = line[1]

            if point == 'center':
                cur_position = [float(line[2]), float(line[3])]
            elif point == 'topleft':
                cur_position = tlwh2xywh([float(line[2]), float(line[3]), float(line[4]), float(line[5])])[0:2]

            if last_position[gender] is None:
                # initiation
                last_position[gender] = cur_position
            else:
                cur_veloctiy = cal_veloctiy(last_position[gender], cur_position, fps)
                # update
                last_position[gender] = cur_position
                if cur_veloctiy > maximum:
                    velocity[gender].append(velocity[gender][-1])
                else:
                    velocity[gender].append(cur_veloctiy)

    # male
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(velocity[male], color='r', label='male')
    plt.hlines(np.mean(velocity[male]), 0, len(velocity[male]),
               label='mean_velocity:{}'.format(np.mean(velocity[male])))
    plt.title('male')
    plt.xlabel('frames')
    plt.ylabel('velocity')
    plt.legend()

    # female
    plt.subplot(1, 2, 2)
    plt.plot(velocity[female], color='r', label='female_label')
    plt.hlines(np.mean(velocity[female]), 0, len(velocity[female]),
               label='mean_velocity:{}'.format(np.mean(velocity[female])))
    plt.title('female')
    plt.xlabel('frames')
    plt.ylabel('velocity')
    plt.legend()
    plt.savefig('./')


if __name__ == "__main__":
    opt = parse_opt()
    cal_vel(**vars(opt))
