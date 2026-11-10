"""
generate LoRa signal

input: parameters of LoRa
output: simulation of LoRa

prepared for visualization UI
"""

"""
python ./SignalGenerator.py `
    --message "HelloWorld" `

python ./SignalGenerator.py `
    --message ./test.txt `
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


parser = argparse.ArgumentParser(description="params of LoRa")
parser.add_argument("--message", type=parse_m, help="message to send")
parser.add_argument("--fs", type=int, default=10e4, help="sample rate, 单位:Hz")
parser.add_argument("--bps", type=int, default=1000, help="bits per second, 单位:bps")
# parser.add_argument("--", type=, default=, help="")
parser.add_argument("--pl", type=int, default=81, help="package length")
parser.add_argument("--SF", type=int, default=7, help="扩频因子")

args = parser.parse_args()
m = args.message
fs = args.fs
bps = args.bps
pl = args.pl
sf = args.SF

samples_per_bit = fs // bps
if samples_per_bit < 1:
    raise ValueError("采样率必须大于 bps")

def crc16_ccitt(data: bytes):
    crc = 0xFFFF
    polynomial = 0x1021
    for byte in data:
        crc ^= byte<<8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc << 1 
        crc &= 0xFFFF
    return crc

# bit mapping: message -> bits
byte_m = str(m).encode("utf-8") # str to bytes
print(f"文本字节数: {len(byte_m)}bytes")

packets = []
for i, start in enumerate(range(0, len(byte_m), pl)):
    packet = byte_m[start:start + pl]
    # whitening: bits after CRC -> Pseudorandom sequence
    
    #crc
    crc = crc16_ccitt(packet)
    crc_packet = packet + crc.to_bytes(2, byteorder="big")

    # channel encoding: eg. 101 -> 111 000 111
    bit_p = "".join(f"{byte:08b}" for byte in crc_packet) #byte to str
    bits = np.fromiter((int(bit) for bit in bit_p), dtype=np.uint8) # str to uint8
    coded_bits = np.repeat(bits, 3)

    # interleaving: -> bits after interleaving
    interleaved_bits = coded_bits.reshape(-1, 3).T.reshape(-1)

    # symbol mapping: bit -> symbol(just label, not val)
    
    # chirp: variable frequence cos(not specific symbol wave, but a template of all symbol chirp)
    # LoRa modulation(give each symbol a chirp): symbol ->baseband
    # RF: baseband -> radio band
    packets.append(packet)

# print(len(packets))
# print(f"文本bit数: {len(bits)}bits")
# waveform = np.repeat(bits, samples_per_bit)
# t_wave = np.arange(len(waveform)) / fs
# print(f"信号仿真时长: {len(t_wave) / fs}s")

