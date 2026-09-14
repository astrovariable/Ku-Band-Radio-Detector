/*
 * ZSD solar detector - simple logger
 * ==================================
 * Prints ONE averaged reading per second. Nothing else.
 * No modes, no baseline, no buzzer - just the measurement.
 *
 * WIRING
 *   AD8318 VCC -> +12 V
 *   AD8318 GND -> 12 V negative AND Arduino GND
 *   AD8318 OUT -> Arduino A0
 *
 * OUTPUT
 *   One number per line = averaged ADC counts (0-1023).
 *   Exactly one line per second, so line number = seconds elapsed.
 *   Works directly in Serial Plotter (one clean trace) and in any
 *   logging terminal (one clean column).
 *
 * READING THE NUMBERS
 *   1 count  = 4.888 mV = 0.196 dB
 *   1 dB     = 5.115 counts
 *   The AD8318 is INVERTED: more signal = FEWER counts.
 *   So a dip in the trace is a rise in received power.
 *
 *   To convert a change to dB:  dB = (counts_before - counts_after) / 5.115
 */

const int PIN_DET = A0;

const int N_AVG = 800;              // samples per reading (~90 ms of sampling)
const unsigned long PERIOD_MS = 1000;   // one reading per second

// Set to true to print dB relative to REF_COUNTS instead of raw counts.
const bool PRINT_DB   = false;
const float REF_COUNTS = 410.0;     // your no-signal level, for the dB option

unsigned long nextRead = 0;

void setup() {
  Serial.begin(115200);
  nextRead = millis();
}

void loop() {
  if (millis() < nextRead) return;
  nextRead += PERIOD_MS;

  long sum = 0;
  for (int i = 0; i < N_AVG; i++) sum += analogRead(PIN_DET);
  float counts = (float)sum / N_AVG;

  if (PRINT_DB) Serial.println((REF_COUNTS - counts) / 5.115, 3);
  else          Serial.println(counts, 2);
}
