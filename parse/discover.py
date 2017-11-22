"""Launch discovery and parsing of logs."""
import os

from .log.fio import FioLog
from .log.netperf import NetperfLog
from .log.stress_ng import StressNgLog
from .log.systemd import SystemdLog


def launch(log_dir):
    """TODO."""
    print(log_dir)

    for release in list_dirs(log_dir):
        print(release)
        release_dir = os.path.join(log_dir, release)

        report_systemd(release_dir)
        gather_results(StressNgLog, os.path.join(release_dir, 'stress-ng'))
        gather_results(NetperfLog, os.path.join(release_dir, 'netperf'))
        gather_results(FioLog, os.path.join(release_dir, 'fio'))


def list_files(path):
    """List all files in a directory."""
    files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            files.append(file_path)

    return sorted(files)


def list_dirs(path):
    """List all directories in a directory."""
    dirs = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            dirs.append(file_path)

    return sorted(dirs)


def report_systemd(release_dir):
    """TODO."""
    results = []
    boot_dir = os.path.join(release_dir, 'boot')

    if not os.path.exists(boot_dir):
        return results

    print('analyzing boot times')
    for boot in list_dirs(boot_dir):
        boot_log_dir = os.path.join(boot_dir, boot)
        for file in list_files(boot_log_dir):
            if file == 'systemd_time.log':
                results.append(SystemdLog(os.path.join(boot_log_dir, file)))

    return results


def gather_results(log_object, directory):
    """Collect results for specific object."""
    results = []
    if not os.path.exists(directory):
        return results

    for file in list_files(directory):
        results.append(log_object(os.path.join(directory, file)))

    return results
