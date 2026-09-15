# ZSD Solar Radio Dish

A home-built 650 mm parabolic dish that detects the Sun's radio signal using a satellite TV LNB. It was made to mark the **Zero Shadow Day (ZSD)** moment, when the Sun passes straight overhead at noon, even when clouds hide the Sun.

This repository contains:

1. **`Parabolic_Dish.cdr`** – the laser-cutting drawing for the dish (CorelDRAW).
2. **`zsd_logger.ino`** – the Arduino sketch that reads the detector once per second.
3. **`zsd_tool.py`** – a Python program that records the readings to a file, plots them, and works out the Sun's transit time.

Created by **Pranshu Kurel**, AstroVariable.

---

## Contents

- [How it works in one paragraph](#how-it-works-in-one-paragraph)
- [Terms used in this project](#terms-used-in-this-project)
- [Dish design](#dish-design)
- [Parts in the cutting drawing](#parts-in-the-cutting-drawing)
- [Building the dish](#building-the-dish)
- [Receiver electronics](#receiver-electronics)
- [Wiring](#wiring)
- [Software setup](#software-setup)
- [Using the Python tool](#using-the-python-tool)
- [Observing a Zero Shadow Day transit](#observing-a-zero-shadow-day-transit)
- [Reading the results](#reading-the-results)
- [Theory](#theory)
- [Safety](#safety)
- [Troubleshooting](#troubleshooting)
- [Files in this repository](#files-in-this-repository)
- [Licence](#licence)

---

## How it works in one paragraph

The Sun gives out radio waves as well as light. The dish collects the radio waves from a small patch of sky and focuses them onto an LNB, the same box used on a DTH satellite TV dish. The LNB amplifies the signal and converts it to a lower frequency that can travel down a coaxial cable. A log detector (AD8318) turns the strength of that signal into a voltage, and an Arduino measures the voltage once per second. If the dish points straight up and stays still, the Sun drifts through its view around noon, and the reading rises and falls. The middle of that rise and fall is the moment the Sun crossed the dish's line of sight. On Zero Shadow Day, that moment is when the Sun is overhead.

---

## Terms used in this project

| Term | Meaning |
|---|---|
| **Zero Shadow Day (ZSD)** | A day when the Sun is exactly overhead at local noon, so upright objects cast no shadow. It happens twice a year at places between the Tropic of Cancer and the Tropic of Capricorn. |
| **Zenith** | The point in the sky straight above you. |
| **Transit** | The moment the Sun (or a star) crosses the north–south line in the sky. For a dish pointing at the zenith, it is when the Sun passes through the centre of the dish's view. |
| **Drift scan** | An observation where the dish is kept still and the Earth's rotation carries the Sun across the dish's view. |
| **Parabola / paraboloid** | A curve (and the 3D bowl made by spinning it) that reflects all waves arriving parallel to its axis to a single point. |
| **Focus / focal length (f)** | The point where the reflected waves meet, and its distance from the centre (vertex) of the dish. |
| **Vertex** | The deepest point at the centre of the dish's curve. |
| **Aperture (D)** | The diameter of the dish opening. |
| **f/D** | Focal length divided by diameter. A small f/D means a deep dish with the focus close in. |
| **Prime focus** | A design where the receiver sits at the focus, in front of the dish's centre. (Most DTH dishes are "offset" instead, with the receiver off to one side.) |
| **Rib** | A curved strip cut to the parabola shape. Several ribs set around a centre form the dish frame. |
| **Hub plate** | The flat round base that holds the ribs in position. |
| **Mesh** | A sheet of woven metal wires with small open holes. Radio waves much longer than the holes are reflected as if the mesh were a solid sheet. Mesh with hole size less than 2 mm was used.  |
| **Segment** | One piece of the reflecting surface. Here, each mesh segment fills the wedge-shaped gap between two neighbouring ribs. |
| **Strut** | A support that holds the LNB at the focus. |
| **LNB** | Low-Noise Block downconverter. The unit at the focus of a satellite dish. It amplifies the weak signal and shifts it down from about 11–12 GHz to about 1–2 GHz. |
| **Ku band** | The radio band from about 12 to 18 GHz by strict definition; in satellite TV the name is used for about 10.7–12.75 GHz. |
| **GHz / MHz** | Gigahertz (billion cycles per second) and megahertz (million cycles per second), units of frequency. |
| **Wavelength (λ)** | The length of one radio wave. At 11 GHz it is about 2.7 cm. |
| **IF** | Intermediate Frequency. The lower frequency (about 950–2150 MHz) that comes out of the LNB. |
| **Bias tee** | A small device that sends DC power up a coaxial cable to the LNB while letting the radio signal come back down to a separate port. |
| **Coax (RG6)** | Coaxial cable, the round shielded cable used for satellite and cable TV. |
| **F connector / SMA connector** | Screw-on connectors. F is used on TV cables; SMA is a smaller one used on radio modules. |
| **Log detector (AD8318)** | A chip that gives a DC voltage in proportion to signal power measured in decibels. The AD8318 output falls by about 25 mV for every 1 dB more power. |
| **Decibel (dB)** | A way of comparing two powers. +3 dB is about twice the power; +10 dB is ten times. |
| **ADC / counts** | The Arduino's analog-to-digital converter turns a voltage into a whole number from 0 to 1023, called "counts". On a 5 V Arduino, 1 count ≈ 4.888 mV. |
| **Baseline** | The reading when the dish sees only empty (cold) sky, used as the zero level. |
| **Beamwidth / FWHM** | How wide a patch of sky the dish sees. FWHM (Full Width at Half Maximum) is the width across which the received power is at least half its peak value. |
| **Half-power points** | The two times, on either side of the peak, when the signal is half its peak value in power. |
| **Serial port (COM port)** | The connection the Arduino uses to send text to the computer over USB. |
| **CSV** | Comma-Separated Values. A plain text table that opens in a spreadsheet. |

---

## Dish design

| Property | Value |
|---|---|
| Type | Prime-focus paraboloid |
| Aperture (D) | 650 mm |
| Focal length (f) | 260 mm |
| f/D | 0.40 |
| Depth at the centre | 101.6 mm (from `D² ÷ 16f`) |
| Frame | 15 laser-cut ribs on a round hub plate |
| Reflecting surface | Metal mesh, cut into 15 segments (one between each pair of neighbouring ribs) |
| Receiver | Ku-band LNB at the focus, held by 3 struts |
| Estimated beamwidth | about 3° (see [Theory](#theory)) |

The dish points where it faces: the LNB sits on the dish's axis, so an audience can see exactly which part of the sky it is looking at.

### Rib shape

The top edge of each rib follows the parabola:

```
z = r² ÷ (4 × f) = r² ÷ 1040
```

where `r` is the distance from the dish axis and `z` is the height of the curve above the vertex, both in millimetres.

Each rib covers `r = 30 mm` to `r = 325 mm`. Checked against the drawing, the rib curve matches `f = 260 mm` to better than 0.001 mm.

### Where the focus is

The ribs do not reach the centre, so the vertex is not a physical point you can measure from. Using the drawing:

- The vertex lies **29.1 mm above the top face of the hub plate**.
- The focus is therefore **289.1 mm above the top face of the hub plate**, on the dish axis.
- The rim is 130.7 mm above the hub plate, so the focus is about **158 mm above the plane of the rim**.

Use these as the starting position for the LNB, then fine-tune by signal strength (see [Building the dish](#building-the-dish), step 13).

---

## Parts in the cutting drawing

All parts in `Parabolic_Dish.cdr` are drawn at full size in millimetres, as red outlines for laser cutting. The slots are 3.9–4.1 mm wide, so the drawing suits sheet material about 4 mm thick.

| Part | Qty | Size (approx.) | Features |
|---|---|---|---|
| **Hub plate** | 1 | Ø670 mm disc | 30 slots (20 × 3.9 mm) in 15 pairs, one pair every 24°. In each pair, one slot is centred 45 mm from the centre and one 285 mm from the centre. |
| **Plain rib** | 12 | 295 × 137 mm | Parabolic top edge. Two tabs (20 × 6 mm) on the bottom edge, 240 mm apart, that fit a slot pair in the hub plate. Two small notches (4 mm wide, 2 mm deep) on the curved edge, at about r = 159 mm and r = 249 mm. |
| **Strut rib** | 3 | 305 × 137 mm | Same as a plain rib, plus an extra tab (10 × 20 mm) sticking out of the outer end. |
| **Strut** | 3 | 330 × 35 mm | Ends cut at about 60°, with a 20 mm wide tab at each end. |
| **LNB mount base** | 1 | Triangle, about 121 mm sides | Ø50 mm hole in the centre; finger joints on all three edges. |
| **LNB mount wall** | 3 | 130 × 44 mm | Finger joints on three edges; one 4 × 20 mm slot in the middle for a strut tab. |
| **Strut bracket** | 3 | 25 × 125 mm | Two 3.9 × 20 mm slots, 85 mm apart centre to centre. |

**About the file:** it was saved in a recent version of CorelDRAW, so older CorelDRAW versions and other programs may not open it. If you share the design, also export a DXF or SVG copy (in CorelDRAW: **File → Export**) and add it to the repository.

---

## Building the dish

1. **Cut a test piece first.** Cut one slot and one tab on scrap sheet. Check the tab pushes into the slot firmly by hand. Laser kerf (the width of material burnt away) changes the fit, so adjust the laser settings or scale before cutting everything.
2. **Cut all parts** listed in the table above.
3. **Lay the hub plate flat** on a level table.
4. **Fit the ribs.** Push each rib's two bottom tabs into a slot pair: the tab near the short end goes into the inner slot (45 mm from centre) and the other tab into the outer slot (285 mm). The curved edge faces up and the tall end faces outward.
5. **Place the three strut ribs** at every fifth slot pair, so they are 120° apart. Their extra end tabs point outward.
6. **Glue** the ribs once they all stand upright and square to the plate. Check with a set square that each rib is vertical.
7. **Build the LNB mount.** Join the three walls to the triangular base with the finger joints, so the walls stand up around the Ø50 mm hole. Glue the joints.
8. **Fit the struts.** Join the lower end of each strut to its strut rib's outer tab using a strut bracket, and push the upper end tab into the slot of one LNB mount wall. Adjust until the mount sits level and centred over the hub plate.
9. **Fit the mesh segments.** The reflecting surface is 15 metal mesh segments, one for each wedge-shaped gap between two neighbouring ribs. Fit one segment at a time: lay it over its two ribs, press it down so it follows the rib curves, and fix it along both rib edges. Work from the centre outward so the mesh doesn't bunch up near the hub.
10. **Close the joins.** Where two segments meet on a rib, make them touch or overlap slightly. Gaps between segments should be much smaller than the wavelength, ideally no more than 2–3 mm (see [Theory](#theory)).
11. **Check the shape.** Cut a card template to the rib curve (trace a rib). Hold it against the mesh midway between two ribs, where the mesh is least supported, and press out any low or high spots. Bumps larger than about 1–2 mm start to reduce the signal at these wavelengths.
12. **Fit and position the LNB.** Pass the LNB's feed through the Ø50 mm hole so the feed opening faces down into the dish. Set the feed opening about 289 mm above the top face of the hub plate.
13. **Fine-tune the focus.** With the receiver running (see [Wiring](#wiring)), point the dish at the Sun or at a DTH satellite. Move the LNB up and down in small steps, a few millimetres at a time, and fix it where the reading is strongest.

---

## Receiver electronics

Parts used in this build:

| Part | Purpose |
|---|---|
| Ku-band LNB | Receives the signal at the dish focus |
| RG6 coax with F connectors | Carries the signal and DC power between the LNB and the bias tee |
| Bias tee, 10 MHz – 6 GHz | Sends 12 V up the cable to the LNB, passes the signal to the detector |
| SMA adapters and SMA male–male link | Connect the bias tee to the detector |
| AD8318 log detector module | Converts signal power to a voltage |
| Arduino Uno | Measures the voltage and sends readings over USB |
| 12 V DC adaptor | Powers both the LNB (through the bias tee) and the AD8318 module |
| Laptop | Runs `zsd_tool.py` to record and analyse |

The AD8318 works from 1 MHz to 8 GHz, so it covers the LNB's whole output band. It measures the **total** power across that band, which is what a simple radiometer needs.

---

## Wiring

```
                 RG6 coax                         SMA link
  [LNB] ────────────────────► [Bias tee] ───────────────────► [AD8318 RF IN]
                              RF+DC port    RF port                  │
                                   ▲                                 │ OUT
                                   │ DC port                         ▼
  [12 V adaptor] +12 V ────────────┴─────────► AD8318 VCC       [Arduino A0]
                 0 V  ─────────────────────── ► AD8318 GND ───► [Arduino GND]
                                                                     │ USB
                                                                     ▼
                                                                 [Laptop]
```

Step by step:

1. Connect the LNB's F socket to the bias tee port that carries **both** RF and DC (often marked "RF+DC"), using RG6 coax.
2. Connect the 12 V adaptor's positive lead to the bias tee's **DC** input.
3. Connect the bias tee's **RF-only** port to the AD8318 module's RF input, using the SMA link and adapters.
4. Connect the 12 V adaptor's positive lead to the AD8318 module's **VCC**.
5. Connect the 12 V adaptor's negative lead to the AD8318 module's **GND**, and also to the Arduino's **GND**. The shared ground is needed for the Arduino to read the detector voltage correctly.
6. Connect the AD8318 module's **OUT** pin to the Arduino's **A0** pin.
7. Connect the Arduino to the laptop with a USB cable.

**Important:** never connect the AD8318 input directly to the LNB cable. The cable carries 12 V DC, which can damage the detector. Always go through the bias tee's RF-only port.

---

## Software setup

### Arduino sketch (`zsd_logger.ino`)

1. Install the [Arduino IDE](https://www.arduino.cc/en/software) if you don't have it.
2. Open `zsd_logger.ino`. The IDE may ask to put it in a folder of the same name; click **OK**.
3. Check that `PRINT_DB` is set to `false` near the top of the sketch. The Python tool expects raw counts.
4. Choose the board: **Tools → Board → Arduino Uno**.
5. Choose the port: **Tools → Port**, then pick the Arduino's port (for example `COM4` on Windows, or `/dev/ttyACM0` or `/dev/ttyUSB0` on Linux).
6. Click **Upload** (the right-arrow button).
7. To check it works, open **Tools → Serial Plotter**, set the speed to **115200 baud**, and point the dish at the sky and then at the Sun. The trace should dip when the Sun is in view. (The detector is inverted: more signal gives fewer counts.)
8. **Close the Serial Plotter and Serial Monitor** before using the Python tool. Only one program can use the port at a time.

What the sketch does: every second, it reads A0 800 times (taking about 90 ms), averages the readings, and prints one number. So each line is one second.

### Python tool (`zsd_tool.py`)

1. Install Python 3 from [python.org](https://www.python.org/downloads/) if you don't have it. On Windows, tick **Add Python to PATH** during installation.
2. Open a terminal (Command Prompt on Windows) in the folder with `zsd_tool.py`.
3. Install the required packages:
   ```bash
   pip install pyserial matplotlib numpy
   ```
4. **Linux only:** if you get a "permission denied" error on the serial port, add yourself to the `dialout` group, then log out and back in:
   ```bash
   sudo usermod -a -G dialout $USER
   ```

---

## Using the Python tool

The tool has three commands: `record`, `plot` and `analyse`.

### `record` – log readings to a CSV file

```bash
python zsd_tool.py record --port COM4
```

| Option | Meaning | Default |
|---|---|---|
| `--port` | Serial port of the Arduino (required) | – |
| `--baud` | Serial speed | `115200` |
| `--out` | Output file name | `zsd_YYYYMMDD_HHMMSS.csv` |
| `--no-plot` | Record without the live graph | live graph on |

- A live graph shows the signal in dB above the baseline.
- Every 10 seconds the terminal prints the elapsed time, the counts and the dB value.
- Press **Ctrl + C** to stop.
- Each reading is saved to the file straight away, so nothing is lost if the run stops unexpectedly.

The CSV file has three columns:

| Column | Meaning |
|---|---|
| `timestamp` | Laptop clock time of the reading, to the nearest second |
| `seconds` | Seconds since recording started |
| `counts` | Averaged ADC reading from the Arduino |

### `plot` – look at a recording as it is

```bash
python zsd_tool.py plot sun_2026-09-14.csv
python zsd_tool.py plot sun_2026-09-14.csv --from 20 --to 60 --save scan.png
```

| Option | Meaning |
|---|---|
| `--from` | Start of the part to plot, in minutes from the start of the recording |
| `--to` | End of the part to plot, in minutes |
| `--save` | Also save the graph as a PNG image |

This plots raw counts with no baseline, smoothing or fitting. Remember that **lower counts mean more signal**. The terminal also prints the lowest and highest counts and the difference in dB.

### `analyse` – find the transit time

```bash
python zsd_tool.py analyse sun_2026-09-14.csv
```

Example output:

```
file          : sun_2026-09-14.csv
readings      : 3600  over 60.0 min
peak signal   : 4.85 dB  at t = 29.40 min
half-power    : 22.80 and 36.10 min
width (FWHM)  : 13.30 min
TRANSIT at    : 29.45 min after the start of the run
implied beam  : 3.1 deg
```

*(The numbers above are only an illustration of the format.)*

What it does, step by step:

1. **Sets the baseline** from the median of the first 30 readings (or the first tenth of the file, if that is shorter). The dish must be looking at empty sky, not the Sun, at the start of the recording.
2. **Converts counts to dB** above that baseline, using 5.115 counts per dB.
3. **Smooths** the data over about 15 seconds to reduce noise.
4. **Finds the peak** of the smoothed curve.
5. **Finds the half-power points**: walking outward from the peak on both sides, it finds where the signal first drops below half of the peak dB value, and interpolates between readings.
6. **Transit time** = the midpoint between the two half-power times. This is more reliable than the peak itself, because it uses the whole shape of the hump.
7. **Implied beamwidth** = FWHM in minutes × 0.23° per minute (the rate at which the Sun drifts across the zenith on Zero Shadow Day, for a place near 23° N).
8. Shows a graph with the raw data, the smoothed curve, the half-power level and a red dashed line at the transit time.

---

## Observing a Zero Shadow Day transit

### Before the day

1. **Find the ZSD date and the time of local solar noon** for your place (for example with the Surya Saathi tool).
2. **Test the system** on an ordinary day: point the dish at the Sun and then at empty sky, and check that the Sun is clearly above the sky reading.

### On the day

1. **Set up in the open** on a firm, level surface, well before noon.
2. **Point the dish at the zenith.** Place a spirit level across the hub plate (or across the rim) and check it in two directions at right angles. Adjust until the bubble is centred both ways. Accuracy matters: a tilt of 1° towards east or west shifts the measured transit by about 4 minutes.
3. **Sync the laptop clock** with internet time (Windows: **Settings → Time & language → Date & time → Sync now**). The transit time is only as accurate as this clock.
4. **Connect and power everything** as described in [Wiring](#wiring).
5. **Start recording** at least **30–40 minutes before** local solar noon, so the first readings are of empty sky:
   ```bash
   python zsd_tool.py record --port COM4 --out zsd_2027-05-31.csv
   ```
6. **Don't touch or move the dish** during the recording. Keep people from standing in front of it.
7. **Stop recording** 30–40 minutes **after** solar noon, with **Ctrl + C**.

### After the recording

1. Run:
   ```bash
   python zsd_tool.py analyse zsd_2027-05-31.csv
   ```
2. Note the **TRANSIT at** value (in minutes after the start).
3. Open the CSV file and read the `timestamp` in the first data row. This is the start time.
4. **Add** the transit minutes to the start time to get the clock time of transit. For example, a start at 11:40:05 plus 29.45 min (29 min 27 s) gives a transit at 12:09:32.
5. Compare this with the predicted solar noon.

---

## Reading the results

- **A clear hump near noon** means the Sun passed through the beam.
- **Hump height:** on Zero Shadow Day the Sun passes through the centre of the beam, so the hump is at its highest. On days far from ZSD, the Sun passes to the north or south of the zenith, and the hump is lower or missing.
- **Width:** the FWHM in minutes, multiplied by the drift rate, gives the beamwidth. For about a 3° beam, expect a width of about 13 minutes.
- **Clouds:** thin and ordinary clouds make only a small difference at these frequencies. Heavy rain reduces the signal more noticeably.
- **Slow drift in the baseline** is normal (the LNB and detector change a little with temperature). A long recording with sky on both sides of the hump shows how large the drift is.

---

## Theory

### Why a parabola

A parabolic reflector sends every wave that arrives parallel to its axis to the same point, the focus, and all of them arrive there at the same time (in step). That is what lets a 650 mm dish collect a weak signal from a small patch of sky and deliver it to one small feed.

For a dish of diameter `D` and focal length `f`:

```
depth at the centre     d = D² ÷ (16 f)            = 650² ÷ 4160  = 101.6 mm
angle from focus to rim ψ = 2 × atan(D ÷ (4 f))    = 2 × atan(0.625) ≈ 64°
```

The angle ψ is how far off-axis the LNB's feed must "see" to cover the whole dish. LNB feeds are usually designed for shallower dishes, so the outer part of this deeper dish is probably less strongly used. This lowers the effective size a little and can make the beam slightly wider than the estimate below.

### Beamwidth

A rough rule for the half-power beamwidth of a dish is:

```
beamwidth ≈ 70 × λ ÷ D   degrees
```

At about 11 GHz, `λ ≈ 27 mm`, so:

```
beamwidth ≈ 70 × 27 ÷ 650 ≈ 2.9°
```

The Sun is only about 0.5° across, so the dish sees it almost as a point. The Sun's size widens the measured hump by only about 1%.

### Drift rate of the Sun

The Earth turns 15° per hour, or 0.25° per minute. For an object at declination `δ` (its angle north or south of the celestial equator), the rate across the sky is:

```
rate = 0.25 × cos δ   degrees per minute
```

On Zero Shadow Day, the Sun's declination equals your latitude. Near 23° N:

```
rate = 0.25 × cos 23° ≈ 0.23° per minute
```

This is the value `zsd_tool.py` uses. For other places or dates, change the `0.23` in the `analyse` function.

### Surface accuracy

Bumps and wrinkles in the reflector send some of the signal the wrong way. The Ruze formula gives the fraction of signal kept:

```
fraction kept = exp( −(4 π ε ÷ λ)² )
```

where `ε` is the typical (RMS) surface error. At `λ = 27 mm`:

| Typical surface error | Signal kept |
|---|---|
| 0.5 mm | about 95% |
| 1 mm | about 80% |
| 2 mm | about 42% |

So keeping the mesh surface accurate to within about 1 mm makes a real difference.

### Why mesh works as a mirror

A metal mesh reflects radio waves almost as well as a solid sheet, as long as its holes are much smaller than the wavelength. A common guide is that the openings should be smaller than about one-tenth of the wavelength:

```
largest opening ≈ λ ÷ 10 ≈ 27 mm ÷ 10 ≈ 2.7 mm   (at about 11 GHz)
```

Smaller holes reflect better. The same idea applies to gaps where two segments meet: keep them well below this size, or overlap the segments.

Mesh also has practical advantages over a solid sheet. It is lighter, lets wind pass through, and lets rain drain away.

### From counts to decibels

The AD8318 output falls by about 25 mV for each 1 dB increase in input power. The Arduino's ADC gives 5 V over 1023 steps, so 1 count is 4.888 mV:

```
counts per dB = 25 mV ÷ 4.888 mV ≈ 5.115
dB change     = (counts before − counts after) ÷ 5.115
```

The sign is reversed because more signal gives a lower voltage.

---

## Safety

- **Concentrated sunlight.** Metal mesh lets much of the sunlight pass through, so it focuses far less heat than a solid shiny surface. The wires still reflect some light towards the LNB, however. During long runs with the dish pointed at the Sun, touch-check the LNB now and then for heating.
- **Never look along the dish axis towards the Sun** or put your hand or face near the focus when the dish faces the Sun.
- **Public events:** keep visitors from touching the LNB, struts and focus area while the dish is pointed at the Sun.
- **12 V supply:** use a proper adaptor. Keep connections dry and off wet ground.

---

## Troubleshooting

| Problem | Things to check |
|---|---|
| No readings in the Python tool | Close the Arduino Serial Monitor and Serial Plotter. Check the `--port` name. Check the USB cable. |
| "Permission denied" on Linux | Add your user to the `dialout` group (see [Software setup](#software-setup)). |
| Readings don't change between Sun and sky | Check 12 V reaches the LNB (through the bias tee's RF+DC port). Check the SMA link. Check the LNB position at the focus. |
| Readings are random or jump around | Check the ground wire between the 12 V supply and the Arduino. Keep the A0 wire short. |
| The dB values come out negative (a dip instead of a hump) | The recording started with the Sun in view, so the baseline is wrong. Start recording earlier, with the dish seeing only sky. |
| `analyse` says half-power crossings were not found | The recording does not cover the whole hump. Record for longer on both sides of noon. |
| The Python tool reads nonsense numbers | Make sure `PRINT_DB` is `false` in the Arduino sketch. |
| Transit time is several minutes off | Check that the dish is level in both directions and that the laptop clock was synced. |

---

## Files in this repository

```
.
├── Parabolic_Dish.cdr   Laser-cutting drawing (CorelDRAW)
├── zsd_logger.ino       Arduino sketch: one averaged reading per second
├── zsd_tool.py          Python: record, plot and analyse drift scans
└── README.md            This file
```

---

## Licence

The contents of this repository are released under the licence in the [`LICENSE`](LICENSE) file.
