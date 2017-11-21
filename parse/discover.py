"""Launch discovery and parsing of logs."""
import os

from .parsers.netperf import Netperf
from .parsers.fio import Fio
from .parsers.stress_ng import StressNg
from .parsers.systemd import Systemd


def launch(log_dir):
    """TODO."""
    log_dir = os.path.abspath(log_dir)
    print(log_dir)

    releases = [f for f in os.listdir(log_dir) if os.path.isdir(os.path.join(log_dir, f))]
    for release in releases:
        print(release)

        netperf_dir = os.path.join(log_dir, release, 'netperf')
        if os.path.exists(netperf_dir):
            print('netperf')
            results = []
            for f in os.listdir(netperf_dir):
                if os.path.isfile(os.path.join(netperf_dir, f)):
                    results.append(Netperf(os.path.join(netperf_dir, f)))

            for result in results:
                print(result)

        fio_dir = os.path.join(log_dir, release, 'fio')
        if os.path.exists(fio_dir):
            print('fio')
            results = []
            for f in os.listdir(fio_dir):
                if os.path.isfile(os.path.join(fio_dir, f)):
                    results.append(Fio(os.path.join(fio_dir, f)))

            for result in results:
                print(result)

        stress_ng_dir = os.path.join(log_dir, release, 'stress-ng')
        if os.path.exists(stress_ng_dir):
            print('stress-ng')
            results = []
            for f in os.listdir(stress_ng_dir):
                if os.path.isfile(os.path.join(stress_ng_dir, f)):
                    results.append(StressNg(os.path.join(stress_ng_dir, f)))

            for result in results:
                print(result)

        boot_dir = os.path.join(log_dir, release, 'boot')
        if os.path.exists(boot_dir):
            print('boot')
            results = []
            boots = [f for f in os.listdir(boot_dir) if os.path.isdir(os.path.join(boot_dir, f))]
            for boot in boots:
                boot_log_dir = os.path.join(boot_dir, boot)
                for f in os.listdir(boot_log_dir):
                    if f == 'systemd_time.log':
                        results.append(Systemd(os.path.join(boot_log_dir, f)))

            for result in results:
                print(result)
