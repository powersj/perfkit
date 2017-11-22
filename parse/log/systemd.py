"""Parse systemd results."""
import re


class SystemdLog(object):
    """systemd Parsing Object."""

    def __init__(self, log_path):
        """Collect relevant information."""
        self.date = log_path.split('/')[-2]

        with open(log_path) as log:
            lines = log.read()


        # test:
        # Startup finished in 3.802s (firmware) + 4.318s (loader) + 5.291s (kernel) + 2min 2.026s (userspace) = 2min 15.439s

        self.kernel = re.findall(r'([0-9\.]+?)s\s\(kernel\)', lines)[0]
        self.userspace = re.findall(r'([0-9\.]+?)s\s\(userspace\)', lines)[0]
        self.total = round(float(self.kernel) + float(self.userspace), 3)

    def __str__(self):
        """Return CSV of results."""
        return '%s,%s,%s,%s' % (self.date, self.kernel, self.userspace,
                                self.total)
