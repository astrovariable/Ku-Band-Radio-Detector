#!/usr/bin/env python3
"""
ZSD solar radio detector - logger and analyser
==============================================

Works with the zsd_logger.ino sketch, which prints one averaged ADC
reading per second.

RECORD A DRIFT SCAN
    python zsd_tool.py record --port COM4
    python zsd_tool.py record --port COM4 --out sun_2026-09-14.csv --no-plot

    Ctrl-C to stop. The CSV is written as it goes, so nothing is lost
    if the run is interrupted.

ANALYSE A RECORDED SCAN
    python zsd_tool.py analyse sun_2026-09-14.csv

    Reports the peak signal, the half-power width, and the transit time
    from the midpoint of the two half-power crossings.

INSTALL
    pip install pyserial matplotlib numpy
"""

import argparse
import csv
import sys
import time
from datetime import datetime

COUNTS_PER_DB = 5.115   # AD8318: -25 mV/dB, Arduino 4.888 mV/count


# ----------------------------------------------------------------- record

def record(port, baud, outfile, live_plot):
    import serial

    if outfile is None:
        outfile = "zsd_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"

    ser = serial.Serial(port, baud, timeout=5)
    time.sleep(2)          # let the board reset
    ser.reset_input_buffer()

    fh = open(outfile, "w", newline="")
    writer = csv.writer(fh)
    writer.writerow(["timestamp", "seconds", "counts"])

    times, counts = [], []
    t_start = time.time()

    plot = None
    if live_plot:
        plot = _LivePlot()

    print(f"recording to {outfile} - Ctrl-C to stop")
    try:
        while True:
            raw = ser.readline().decode("ascii", "ignore").strip()
            if not raw:
                continue
            try:
                c = float(raw)
            except ValueError:
                continue        # skip any stray text

            t = time.time() - t_start
            writer.writerow([datetime.now().isoformat(timespec="seconds"),
                             round(t, 1), c])
            fh.flush()

            times.append(t)
            counts.append(c)

            if plot:
                plot.update(times, counts)

            if len(counts) % 10 == 0:
                db = _to_db(counts)
                print(f"  {t:7.0f} s   {c:7.2f} counts   {db[-1]:+.2f} dB")

    except KeyboardInterrupt:
        print(f"\nstopped. {len(counts)} readings saved to {outfile}")
    finally:
        fh.close()
        ser.close()


def _to_db(counts, n_base=30):
    """Convert a counts series to dB above the opening baseline.
    Fewer counts = more signal, hence the sign."""
    import numpy as np
    c = np.asarray(counts, dtype=float)
    n = min(n_base, max(1, len(c) // 10))
    base = np.median(c[:n])
    return (base - c) / COUNTS_PER_DB


class _LivePlot:
    def __init__(self):
        import matplotlib.pyplot as plt
        self.plt = plt
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(9, 4.5))
        self.line, = self.ax.plot([], [], lw=1.2)
        self.ax.set_xlabel("minutes")
        self.ax.set_ylabel("dB above baseline")
        self.ax.grid(alpha=0.3)
        self.fig.tight_layout()

    def update(self, times, counts):
        if len(counts) < 5:
            return
        db = _to_db(counts)
        mins = [t / 60.0 for t in times]
        self.line.set_data(mins, db)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()


# ------------------------------------------------------------- plain plot

def plot_file(path, t_from, t_to, save):
    """Just plot the recorded counts. No baseline, no smoothing, no fitting."""
    import matplotlib.pyplot as plt

    t, c = [], []
    with open(path) as fh:
        for row in csv.DictReader(fh):
            mins = float(row["seconds"]) / 60.0
            if t_from is not None and mins < t_from:
                continue
            if t_to is not None and mins > t_to:
                continue
            t.append(mins)
            c.append(float(row["counts"]))

    if not t:
        print("no readings in that interval")
        return

    span = max(c) - min(c)
    print(f"{len(t)} readings   {t[0]:.1f} to {t[-1]:.1f} min")
    print(f"counts: min {min(c):.2f}  max {max(c):.2f}  "
          f"range {span:.2f} counts = {span/COUNTS_PER_DB:.2f} dB")

    plt.figure(figsize=(10, 4.5))
    plt.plot(t, c, lw=0.9)
    plt.xlabel("minutes since start of recording")
    plt.ylabel("ADC counts  (lower = more signal)")
    plt.title(path)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if save:
        plt.savefig(save, dpi=130)
        print(f"saved {save}")
    plt.show()


# ---------------------------------------------------------------- analyse

def analyse(path):
    import numpy as np
    import matplotlib.pyplot as plt

    t, c = [], []
    with open(path) as fh:
        for row in csv.DictReader(fh):
            t.append(float(row["seconds"]))
            c.append(float(row["counts"]))
    t = np.asarray(t)
    db = _to_db(c)

    # smooth over ~15 s to take the edge off the noise
    w = max(3, int(15 / max(np.median(np.diff(t)), 0.1)))
    kernel = np.ones(w) / w
    sm = np.convolve(db, kernel, mode="same")
    # convolution edges are unreliable
    sm[:w] = db[:w]
    sm[-w:] = db[-w:]

    peak_i = int(np.argmax(sm))
    peak_db = sm[peak_i]
    half = peak_db / 2.0

    def crossing(lo, hi, step):
        """Walk out from the peak until the curve drops below half power."""
        for i in range(lo, hi, step):
            if sm[i] < half:
                # linear interpolation between this point and the previous
                j = i - step
                f = (half - sm[i]) / (sm[j] - sm[i])
                return t[i] + f * (t[j] - t[i])
        return None

    t_rise = crossing(peak_i, 0, -1)
    t_fall = crossing(peak_i, len(sm), 1)

    print(f"\nfile          : {path}")
    print(f"readings      : {len(t)}  over {t[-1]/60:.1f} min")
    print(f"peak signal   : {peak_db:.2f} dB  at t = {t[peak_i]/60:.2f} min")

    if t_rise is not None and t_fall is not None:
        mid = 0.5 * (t_rise + t_fall)
        print(f"half-power    : {t_rise/60:.2f} and {t_fall/60:.2f} min")
        print(f"width (FWHM)  : {(t_fall - t_rise)/60:.2f} min")
        print(f"TRANSIT at    : {mid/60:.2f} min after the start of the run")
        beam = (t_fall - t_rise) / 60.0 * 0.23   # ~0.23 deg/min at ZSD
        print(f"implied beam  : {beam:.1f} deg")
    else:
        print("half-power crossings not found - the scan may not cover the")
        print("full hump, or the signal is too weak to fit.")
        mid = None

    plt.figure(figsize=(9, 4.5))
    plt.plot(t / 60, db, lw=0.8, alpha=0.4, label="raw")
    plt.plot(t / 60, sm, lw=1.6, label="smoothed")
    if mid is not None:
        plt.axhline(half, ls=":", lw=1, color="gray")
        plt.axvline(mid / 60, ls="--", lw=1.2, color="crimson", label="transit")
    plt.xlabel("minutes since start")
    plt.ylabel("dB above baseline")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


# -------------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description="ZSD solar detector logger")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("record", help="log serial data to CSV")
    r.add_argument("--port", required=True, help="e.g. COM4 or /dev/ttyUSB0")
    r.add_argument("--baud", type=int, default=115200)
    r.add_argument("--out", default=None, help="output CSV filename")
    r.add_argument("--no-plot", action="store_true", help="log without a live plot")

    g = sub.add_parser("plot", help="just plot a recorded file")
    g.add_argument("file")
    g.add_argument("--from", dest="t_from", type=float, default=None,
                   help="start of interval, in minutes")
    g.add_argument("--to", dest="t_to", type=float, default=None,
                   help="end of interval, in minutes")
    g.add_argument("--save", default=None, help="also save a PNG")

    a = sub.add_parser("analyse", help="fit a drift scan (for later)")
    a.add_argument("file")

    args = p.parse_args()
    if args.cmd == "record":
        record(args.port, args.baud, args.out, not args.no_plot)
    elif args.cmd == "plot":
        plot_file(args.file, args.t_from, args.t_to, args.save)
    else:
        analyse(args.file)


if __name__ == "__main__":
    main()
