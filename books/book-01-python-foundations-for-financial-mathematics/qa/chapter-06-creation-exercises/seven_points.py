"""Supplemental construction example; no valuation/workspace replacement."""
import numpy as np

def main():
    shifts = np.linspace(-0.015, 0.015, num=7, endpoint=True, dtype=np.float64)
    observation_index = np.arange(7, dtype=np.int64)
    print('Shift grid:', [f'{x:.3f}' for x in shifts])
    print('Count:', shifts.size)
    print('Observation positions:', observation_index.tolist())
    print('Index dtype:', observation_index.dtype)

if __name__ == '__main__':
    main()
