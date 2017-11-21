"""Parse stress-ng results."""
import re


class StressNg(object):
    """StressNg Parsing Object."""

    def __init__(self, log_path):
        """Collect relevant information."""
        self.date = log_path.split('/')[-1].split('-')[1].replace('.log', '')
        with open(log_path) as f:
            lines = f.read()

        regex = r'stress-ng:\sinfo:\s+\[\d+\]\smatrix\s+(.+?)\n'
        match = re.search(regex, lines)
        group = match.group(1)
        self.bogo_ops_real = ' '.join(group.split()).split(' ')[4]

    def __str__(self):
        """Return CSV of results."""
        return '%s,%s' % (self.date, self.bogo_ops_real)
