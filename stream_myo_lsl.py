from matplotlib import pyplot as plt
from collections import deque

import collections
import time
import sys

import myo
import numpy as np

import pylsl


class EmgCollector(myo.DeviceListener):
  """
  Collects EMG data in a queue with *n* maximum number of elements.
  """

  def __init__(self, n, streamer):
    self.times = collections.deque()
    self.last_time = None
    self.n = n

    self.streamer = streamer
    self.emg_data_queue = deque(maxlen=n)
  
  @property
  def rate(self):
    if not self.times:
      return 0.0
    else:
      return 1.0 / (sum(self.times) / float(self.n))

  def get_emg_data(self):
    with self.lock:
      return list(self.emg_data_queue)

  # myo.DeviceListener

  def on_connected(self, event):
    event.device.stream_emg(True)

  def on_emg(self, event):
    t = time.perf_counter()
    if self.last_time is not None:
      self.times.append(t - self.last_time)
      if len(self.times) > self.n:
        self.times.popleft()
    self.last_time = t

    self.streamer.stream_data(event.emg)

class StreamerLSL(object):

  def __init__(self):
    infoEMG = pylsl.StreamInfo('emg', 'EMG', 8, 200, 'int32', 'EMG-MYO')
    self.outletEMG = pylsl.StreamOutlet(infoEMG)

  def stream_data(self, emg, timestamp):
    self.outletEMG.push_sample(emg, timestamp=timestamp)
  
  def stream_data(self, emg):
    self.outletEMG.push_sample(emg)

def main():
  myo.init()
  hub = myo.Hub()
  streamer = StreamerLSL()
  listener = EmgCollector(50, streamer)
  print("Streaming through LSL...")
  while hub.run(listener.on_event, 500):
    print("\r\033[KEMG Rate:", listener.rate, end='')
    sys.stdout.flush()


if __name__ == '__main__':
  main()
