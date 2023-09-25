from datetime import datetime
import pprint
from time import sleep
import requests
import csv


if __name__ == "__main__":
    with open(f"stats-{datetime.now()}.csv", "w") as stat_file:
        csv_writer = csv.DictWriter(
            stat_file,
            fieldnames=[
                "time",
                "cd_status",
                "cd_eclapsed",
                "net_status",
                "net_elapsed",
                "gpsLat",
                "gpsLng",
                "altitude",
                "speed",
            ],
            extrasaction="ignore",
        )
        csv_writer.writeheader()
        while True:
            row_data = {"time": datetime.now()}
            print("=== Tick ===")
            # CD data
            try:
                cd_data = requests.get(
                    "http://cdwifi.cz/portal/api/vehicle/realtime", timeout=5
                )
                row_data["cd_status"] = cd_data.status_code
                row_data["cd_eclapsed"] = cd_data.elapsed.total_seconds()
                row_data |= cd_data.json()
            except Exception as e:
                pprint.pprint(e)
            # Network data
            try:
                net_data = requests.get(
                    "http://detectportal.firefox.com/canonical.html", timeout=5
                )
                row_data["net_status"] = net_data.status_code
                row_data["net_elapsed"] = net_data.elapsed.total_seconds()
            except Exception as e:
                pprint.pprint(e)
            # Print resources
            pprint.pprint(row_data)
            csv_writer.writerow(row_data)
            stat_file.flush()
            sleep(5)
