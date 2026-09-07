"""
Sample files in the ADCON Somalia CSV export format for the documentation
screenshot harness. Run inside the mock FTP source at start (SAMPLE_ROOT,
SAMPLE_TZ, SAMPLE_HOURS in the environment): one CSV per station and day,
named <station id>-<YYYYMMDD>.csv, with the day's 15-minute rows in the layout
the decoder documents. Nothing here is real data.
"""

import math
import os
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ROOT = os.environ.get("SAMPLE_ROOT", "/srv/ftp")
TZ = ZoneInfo(os.environ.get("SAMPLE_TZ", "Africa/Mogadishu"))
HOURS = int(os.environ.get("SAMPLE_HOURS", "48"))

STATIONS = ["516877", "516878", "516879"]
HEADER = ("StationID,Date,Time,Time zone,Barometric Pressure,Global Radiation,Precipitation,"
          "Relative Humidity,Temperature,Dew point,Wind Direction,Wind Speed,Battery Voltage")


def row(station, moment):
    rng = random.Random(f"{station}-{moment:%Y%m%d%H%M}")
    hour = moment.hour + moment.minute / 60
    diurnal = math.sin((hour - 9) / 24 * 2 * math.pi)
    temp = 27 + 5 * diurnal + rng.uniform(-0.4, 0.4)
    rh = 65 - 18 * diurnal + rng.uniform(-2, 2)
    dew = temp - (100 - rh) / 5
    solar = max(0.0, 900 * math.sin((hour - 6) / 12 * math.pi)) if 6 <= hour <= 18 else 0
    rain = rng.choice([0, 0, 0, 0, 0, 0.2, 0.4]) if 14 <= hour <= 17 else 0
    return ",".join([
        station,
        moment.strftime("%d/%m/%Y"),
        moment.strftime("%H:%M:%S"),
        "EAT",
        f"{969 + 1.5 * math.sin(hour / 12 * math.pi) + rng.uniform(-0.3, 0.3):.1f}",
        f"{solar:.1f}",
        f"{rain:.1f}",
        f"{rh:.1f}",
        f"{temp:.1f}",
        f"{dew:.1f}",
        f"{(95 + 30 * diurnal + rng.uniform(-15, 15)) % 360:.1f}",
        f"{max(0.0, 9 + 4 * diurnal + rng.uniform(-1, 1)):.1f}",
        f"{6.6 + rng.uniform(-0.05, 0.05):.2f}",
    ])


def main():
    now = datetime.now(TZ).replace(second=0, microsecond=0)
    now -= timedelta(minutes=now.minute % 15)
    start = now - timedelta(hours=HOURS)
    moments = [start + timedelta(minutes=15 * i) for i in range(HOURS * 4 + 1)]
    by_day = {}
    for m in moments:
        by_day.setdefault(m.date(), []).append(m)

    for station in STATIONS:
        for day, day_moments in by_day.items():
            path = f"{ROOT}/adcon-som/{station}-{day:%Y%m%d}.csv"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", newline="") as f:
                f.write(HEADER + "\r\n")
                for m in day_moments:
                    f.write(row(station, m) + "\r\n")
    print(f"[mock-ftp] adcon-som samples for {len(STATIONS)} stations, {len(by_day)} day(s)", flush=True)


if __name__ == "__main__":
    main()
