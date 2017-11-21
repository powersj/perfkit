"""Parse systemd results."""
import re


class Systemd(object):
    """systemd Parsing Object."""

    def __init__(self, log_path):
        """Collect relevant information."""
        self.date = log_path.split('/')[-2]
        with open(log_path) as f:
            lines = f.read()

        self.kernel = re.findall(r'([0-9\.]+?)s\s\(kernel\)', lines)[0]
        self.userspace = re.findall(r'([0-9\.]+?)s\s\(userspace\)', lines)[0]
        self.total = round(float(self.kernel) + float(self.userspace), 3)

    def __str__(self):
        """Return CSV of results."""
        return '%s,%s,%s,%s' % (self.date, self.kernel, self.userspace,
                                self.total)
