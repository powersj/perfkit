"""Parse systemd results."""


class SystemdAnalyzeLog(object):
    """systemd Parsing Object."""

    name = 'systemd-analyze'

    def __init__(self, log_path):
        """Collect relevant information."""
        self.times = {
            'firmware': 0.0,
            'loader': 0.0,
            'kernel': 0.0,
            'userspace': 0.0
        }

        self.date = log_path.split('/')[-1].split('-')[1].replace('.log', '')
        self._parse_times(log_path)
        self.total = round(sum(self.times.values()), 3)

    def __str__(self):
        """Return CSV of results."""
        return '%s,%s,%s,%s,%s,%s,%s' % (self.name,
                                         self.date,
                                         self.times['firmware'],
                                         self.times['loader'],
                                         self.times['kernel'],
                                         self.times['userspace'],
                                         self.total)

    def _parse_times(self, log_path):
        """Parse out the various times from analyze output."""
        with open(log_path) as log:
            lines = log.read()

        # ['3.802s firmware', '4.318s loader', '5.291s kernel',
        #  '2min 2.026s userspace']
        prefix = 'Startup finished in '
        lines = lines.replace(prefix, '').split('=')[0].split('+')
        results = [x.replace('(', '').replace(')', '').strip() for x in lines]

        for entry in results:
            values = entry.split(' ')

            if len(values) == 3:
                mins = float(values[0].replace('min', ''))
                seconds = float(values[1].replace('s', ''))
                self.times[values[2]] = (mins * 60.0) + seconds
            else:
                self.times[values[1]] = float(values[0].replace('s', ''))


class RebootLog(SystemdAnalyzeLog):
    """TODO."""

    name = 'reboot'

    def __init__(self, log_path):
        """TODO."""
        super(RebootLog, self).__init__(log_path)
