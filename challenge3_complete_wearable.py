import glob
from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from Python.ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.IdleDetector import IdleDetector
from ECE16Lib.Pedometer import Pedometer
from matplotlib import pyplot as plt
import time
from pyowm import OWM
import datetime


# Retrieve a list of the names of the subjects
def get_subjects(directory):
    filepaths = glob.glob(directory + "\\*")
    return [filepath.split("\\")[-1] for filepath in filepaths]


# setup Open Weather API
def weather_setup():
    owm = OWM('63642c0af254a8ecddd0188c58f2a83b').weather_manager()
    weather = owm.weather_at_place('San Diego,CA,US').weather
    return weather


def get_time_and_date():
    # get time and date
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    current_time = "Time: " + str(current_time)
    current_date = now.strftime("%m-%d")
    current_date = "Date: " + str(current_date)
    return current_time, current_date


def get_weather(weather):
    # Get weather
    message = weather.temperature('fahrenheit')
    message = str(message)
    temp = "WX: " + message[9:13]
    return temp


if __name__ == "__main__":
    fs = 50  # sampling rate
    num_samples = 500  # 10 seconds of data @ 50Hz
    refresh_time = 1  # plot every second

    times = CircularList([], num_samples)
    # ax = CircularList([], num_samples)
    # ay = CircularList([], num_samples)
    # az = CircularList([], num_samples)
    ppg = CircularList([], num_samples)

    # setup Heart rate monitor
    hr_monitor = HRMonitor(500, 50)
    hr_monitor.train(fs)

    # setup pedometer
    ped = Pedometer(250, fs, [])

    # setup weather
    weather = weather_setup()

    # setup idleDetector
    idle_detector = IdleDetector(10000)

    # setup communication
    comms = Communication("COM4", 115200)
    comms.clear()  # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data
    time.sleep(3)

    wx = get_weather(weather)
    comms.send_message(wx)

    try:
        previous_time = time.time()
        previous_weather = time.time()

        while True:
            message = comms.receive_message()
            if message is not None:
                try:
                    (m1, m2, m3, m4, m5) = message.split(',')
                except ValueError:  # if corrupted data, skip the sample
                    continue

                # add the new values to the circular lists
                times.add(int(m1) / 1e3)
                # ax.add(int(m2))
                # ay.add(int(m3))
                # az.add(int(m4))
                ppg.add(int(m5))
                ped.add(int(m2), int(m3), int(m4))

                # if enough time has elapsed, clear the axes, and plot the 4 plots
                current_time = time.time()
                if current_time - previous_time > refresh_time:
                    previous_time = current_time

                    # send HR to MCU
                    hr = hr_monitor.predict(ppg, fs)
                    message = "HR: " + str(format(hr, '.0f')) + " BPM"
                    comms.send_message(message)

                    # plt.clf()
                    # plt.subplot(411)
                    # plt.plot(ax)
                    # plt.subplot(412)
                    # plt.plot(ay)
                    # plt.subplot(413)
                    # plt.plot(az)
                    # plt.subplot(414)
                    # plt.plot(ppg)
                    # plt.show(block=False)
                    # plt.pause(0.0001)

                    # send Steps to MCU
                    steps, peaks, filtered = ped.process()
                    print("Step count: {:d}".format(steps))

                    message = "Steps: " + str(steps)
                    comms.send_message(message)

                    plt.cla()
                    plt.plot(filtered)
                    plt.title("Step Count: %d" % steps)
                    plt.show(block=False)
                    plt.pause(0.001)

                    if not idle_detector.check_active(steps):  # if user is meeting pace to goal send alert
                        comms.send_message("User Inactive")
                    else:  # send data and time in are meeting goal
                        # get date and time
                        t, d = get_time_and_date()
                        # send time
                        print(t)
                        comms.send_message(t)
                        time.sleep(0.0001)
                        # send date
                        print(d)
                        comms.send_message(d)
                        time.sleep(0.0001)





                if current_time - previous_weather > 60:
                    previous_weather = current_time

                    # send weather
                    wx = get_weather(weather)
                    print(wx)
                    comms.send_message(wx)
                    time.sleep(0.0001)

    except(Exception, KeyboardInterrupt) as e:
        print(e)  # exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()
