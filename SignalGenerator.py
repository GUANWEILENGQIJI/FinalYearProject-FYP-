"""
generate LoRa signal

input: parameters of LoRa
output: simulation of LoRa

prepared for visualization UI
"""

import numpy as np
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="params of LoRa")
parser.add_argument("--fs", type=int, default=10e4, help="sample rate, 单位:Hz")
parser.add_argument("--duration", type=float, default=0.01, help="simulated signal period, 单位:s")

args = parser.parse_args()
t = np.arange(0, args.duration, 1/args.fs)

# sin wave test
signal = np.sin(2 * np.pi * 1000 * t) #standard sin wave

# chirp: variable frequence cos