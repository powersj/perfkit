"""Launch discovery and parsing of logs."""
import os

from .log.fio import FioLog
from .log.netperf import NetperfLog
from .log.stress_ng import StressNgLog
from .log.systemd import SystemdAnalyzeLog

LOG_TYPES = [SystemdAnalyzeLog, StressNgLog, NetperfLog, FioLog]

def launch(log_dir):
    """TODO."""
    print(log_dir)

    for release in list_dirs(log_dir):
        print(release)
        release_dir = os.path.join(log_dir, release)

        for log_type in LOG_TYPES:
            log_dir = os.path.join(release_dir, log_type.name)
            results = gather_results(log_type, log_dir)
            for result in results:
                print(result)


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


def gather_results(log_object, directory):
    """Collect results for specific object."""
    results = []
    if not os.path.exists(directory):
        return results

    for file in list_files(directory):
        results.append(log_object(os.path.join(directory, file)))

    return results
