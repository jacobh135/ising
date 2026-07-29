import math

lut = []
for i in range (0, 512):
    x = (i - 256) / 32
    p = (1 + math.tanh(x))/2
    num = int(round(p * 4095))
    lut.append(num)

with open("lut.hex", "w") as f:
    for i in lut:
        f.write(f"{i:03x}\n")