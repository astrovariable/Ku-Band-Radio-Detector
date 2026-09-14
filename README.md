# Ku-Band-Radio-Detector
A 650 mm prime-focus parabolic metal mesh dish built to detect the Sun at microwave frequencies, designed so that its beam points along the axis the dish visibly faces — a requirement for outreach use, where an audience should be able to see the instrument aimed at the overhead Sun.

The telescope's intended application is timing the moment of solar transit on Zero Shadow Days, when the Sun passes directly overhead. Because microwaves at this frequency pass through cloud with little attenuation, the measurement succeeds under overcast conditions where the visual phenomenon — the disappearance of shadows — cannot be observed at all.

The reflector is built from fifteen laser-cut MDF ribs slotted into a central hub plate, following the parabola y = r²/1040, with a focal ratio of 0.40, a focal length of 260 mm and a rim depth of 101.6 mm. The reflecting surface is metal mesh laid in tapered gores over the rib frame, with the mesh aperture well inside the quarter-wavelength limit at this band. A commercial Ku-band LNB sits at the prime focus on a three-strut support, giving an expected half-power beamwidth of about 2.8° at 11.7 GHz.

The receiver chain is entirely passive-to-DC: the LNB downconverts 10.7–11.7 GHz to an intermediate frequency of 950–1950 MHz, which passes through a bias tee — supplying the LNB's 12 V over the same coaxial cable — into an AD8318 logarithmic power detector. The detector's output is digitised by an Arduino microcontroller, averaged over 800 samples per second, and logged to a laptop. Because the AD8318 responds to the full IF bandwidth rather than a narrow slice, it offers higher sensitivity than a software-defined radio for total-power work of this kind.

Performance is measured rather than assumed. Hot/cold comparison between ground and zenith sky gives a system temperature of roughly 80–95 K. The Sun raises the received power by 3.33 dB above the cold-sky baseline, against a baseline scatter of 0.2 counts — a detection at better than eighty times the noise. A geostationary satellite gives 6.45 dB. The instrument has also recorded aircraft passing roughly 15° from the pointing axis, detected through antenna sidelobes and confirmed independently against flight-tracking data.

UPDATE: An alt-az mount fabrication for the dish is in progress.
