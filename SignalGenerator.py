"""
generate LoRa signal

input: parameters of LoRa
output: simulation of LoRa

prepared for visualization UI
"""

import numpy as np
import argparse
import matplotlib.pyplot as plt
from pathlib import Path

def parse_m(value: str) -> str:
    path = Path(value)
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return value

"""
python ./SignalGenerator.py `
    --message "HelloWorld" `

python ./SignalGenerator.py `
    --message ./test.txt `
"""
parser = argparse.ArgumentParser(description="params of LoRa")
parser.add_argument("--message", type=parse_m, help="message to send")
parser.add_argument("--fs", type=int, default=10e4, help="sample rate, 单位:Hz")
parser.add_argument("--bps", type=int, default=1000, help="bits per second, 单位:bps")

args = parser.parse_args()
m = args.message
fs = args.fs
bps = args.bps

samples_per_bit = fs // bps
if samples_per_bit < 1:
    raise ValueError("采样率必须大于 bps")

# bit mapping: message -> bits
byte_m = str(m).encode("utf-8") #val type bytes
print(f"文本字节数: {len(byte_m)}bytes")
bit_m = "".join(f"{byte:08b}" for byte in byte_m) #val type str

bits = np.fromiter((int(bit) for bit in bit_m), dtype=np.uint8) #val type uint8
print(f"文本bit数: {len(bits)}bits")
waveform = np.repeat(bits, samples_per_bit)
t_wave = np.arange(len(waveform)) / fs
print(f"信号仿真时长: {len(t_wave) / fs}s")

# CRC: bits -> bits + CRC bits


# whitening: bits after CRC -> Pseudorandom sequence
# channel encoding: eg. 101 -> 111 000 111
# interleaving: -> bits after interleaving
# symbol mapping: bit -> symbol(just label, not val)
# chirp: variable frequence cos(not specific symbol wave, but a template of all symbol chirp)
# LoRa modulation(give each symbol a chirp): symbol ->baseband
#RF: baseband -> radio band