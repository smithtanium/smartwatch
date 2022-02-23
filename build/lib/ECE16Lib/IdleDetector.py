from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
import time
import math
import numpy as np

# # sqrt(x^2 + y^2 + z^3)
# def get_euclidean_distance(x, y, z):
#     x = int(x) ** 2  #
#     y = int(y) ** 2
#     z = int(z) ** 2
#     sum_xyz = x + y + z
#     square_root = math.sqrt(sum_xyz)
#     return square_root
#
# # |x| + |y| + |z|
# def sum_of_abs(x, y, z):
#     x = abs(int(x))
#     y = abs(int(y))
#     z = abs(int(z))
#     return x + y + z


class IdleDetector:
    """
    Encapsulated attributes
    """
    # __comm_name = ""
    # __num_samples = 100  # 2 seconds of data @ 50Hz
    # __refresh_time = 0.3  # update the plot every 0.1s (10 FPS)
    # __last_ax = 0
    # __active = False
    # __log_time = time()
    __steps_per_minute_goal = 0
    __time_last_minute = 0
    __time_init = 0

    def __init__(self, step_goal):
        self.time_init = time.time()
        self.__steps_per_minute_goal = step_goal / 24 / 60
        self.__time_last_minute = time.time()
        # self.__times = CircularList([], self.__num_samples)
        # self.__ax = CircularList([], self.__num_samples)
        # self.__ay = CircularList([], self.__num_samples)
        # self.__az = CircularList([], self.__num_samples)
        # self.__average_x = CircularList([], self.__num_samples)
        # self.__delta_x = CircularList([], self.__num_samples)
        # self.__L1 = CircularList([], self.__num_samples)
        # self.__L2 = CircularList([], self.__num_samples)
        # self.__max_x = CircularList([], self.__num_samples)

    # def setup(self):
        # self.__comm_name = Communication("COM4", 115200)
        # self.__comm_name.clear()  # just in case any junk is in the pipes
        # self.__comm_name.send_message("wearable")  # begin sending data

    def check_active(self, steps):  # checks if outside 40 band buffer
        time_passed = (time.time() - self.time_init) / 60
        steps_per_minute = steps / time_passed

        if steps_per_minute < self.__steps_per_minute_goal:
            return False
        else:
            return True
        # if self.__average_x[-1] + 20 < x:  # most recent reading
        #     return True
        # elif self.__average_x[-1] - 20 > x:  # most recent reading
        #     return True
        # else:
        #     return False

    # def ave_ax(self, val):  # sums all readings and finds mean
    #     sum_ax = np.sum(val)  # sum
    #     average_ax = sum_ax / self.__num_samples  # average
    #     return average_ax

    # def run(self):
        # self.setup()  # setup serial via bluetooth
        # try:
        #     previous_time = 0
        #     while True:
        #         message = self.__comm_name.receive_message()
        #         if message is not None:
        #             try:
        #                 (m1, m2, m3, m4) = message.split(',')
        #             except ValueError:  # if corrupted data, skip the sample
        #                 continue
        #
        #             # add the new values to the circular lists
        #             self.__times.add(int(m1))
        #             self.__ax.add(int(m2))
        #             self.__ay.add(int(m3))
        #             self.__az.add(int(m4))
        #             self.__average_x.add(self.ave_ax(self.__ax))  # adds average
        #             self.__delta_x.add(int(m2) - int(self.__last_ax))  # delta of ax
        #             self.__last_ax = m2  # last ax
        #             self.__L2.add(get_euclidean_distance(int(m2), int(m3), int(m4)))  # gets euclidean distance and adds to L2
        #             self.__L1.add(sum_of_abs(int(m2), int(m3), int(m4)))  # adds the sum of absolute values to L1
        #             # self.__max_x.add(np.amax(int(self.__ax)))
        #
        #             # checks  for activity or inactivity and logs time
        #             if self.check_active(int(m2)) and not self.__active:
        #                 self.__active = True
        #                 self.__log_time = time()
        #             elif not self.check_active(int(m2)) and self.__active:
        #                 self.__active = False
        #                 self.__log_time = time()
        #             # check if 1 or 5 seconds have elapsed.
        #             if self.__active and time() - self.__log_time > 1:
        #                 self.__comm_name.send_message("User Active")
        #                 self.__active = False
        #             elif not self.__active and time() - self.__log_time > 5:
        #                 self.__comm_name.send_message("User Inactive")
        #                 self.__active = True
        #
        #             # if enough time has elapsed, clear the axis, and plot az
        #             current_time = time()
        #             if current_time - previous_time > self.__refresh_time:
        #                 previous_time = current_time
        #
        #                 # # plots ax, ay, az
        #                 # plt.figure(1)
        #                 # plt.subplot(311)
        #                 # plt.plot(self.__ax)
        #                 # plt.title('ax')
        #                 # plt.subplot(312)
        #                 # plt.title('ay')
        #                 # plt.plot(self.__ay)
        #                 # plt.subplot(313)
        #                 # plt.plot(self.__az)
        #                 # plt.title('az')
        #                 # plt.tight_layout()
        #                 # plt.show(block=False)
        #                 # plt.pause(0.001)
        #                 # plt.clf()
        #
        #                 # plots average, delta and L1
        #                 plt.figure(2)
        #                 plt.subplot(311)
        #                 plt.plot(self.__average_x)
        #                 plt.title('average_X')
        #                 plt.subplot(312)
        #                 plt.plot(self.__delta_x)
        #                 plt.title('delta_x')
        #                 plt.subplot(313)
        #                 plt.plot(self.__L1)
        #                 plt.title('L1')
        #                 plt.tight_layout()
        #                 plt.show(block=False)
        #                 plt.pause(0.001)
        #                 plt.clf()
        #
        #                 # # plots L2 and max_x
        #                 # plt.figure(3)
        #                 # plt.subplot(211)
        #                 # plt.plot(self.__L2)
        #                 # plt.title('L2')
        #                 # plt.subplot(212)
        #                 # plt.plot(self.__max_x)
        #                 # plt.title('max_x')
        #                 # plt.tight_layout()
        #                 # plt.show(block=False)
        #                 # plt.pause(0.001)
        #                 # plt.clf()
        # except(Exception, KeyboardInterrupt) as e:
        #     print(e)  # Exiting the program due to exception
        # finally:
        #     self.__comm_name.send_message("sleep")  # stop sending data
        #     self.__comm_name.close()
