"""Parse netperf results."""


class NetperfLog(object):
    """Netperf Parsing Object."""

    name = 'netperf'

    def __init__(self, log_path):
        """Collect relevant information."""
        filename = log_path.split('/')[-1]
        self.protocol = filename.split('-')[0].split('_')[0]
        self.test = filename.split('-')[0].split('_')[1]
        self.date = filename.split('-')[1].replace('.log', '')

        with open(log_path) as log:
            lines = log.read()

        if self.test == 'RR':
            self.result = self._get_result(lines, -3, 5)
        elif self.protocol == 'UDP':
            self.result = self._get_result(lines, -4, 5)
        else:
            self.result = self._get_result(lines, -2, 4)

    @staticmethod
    def _get_result(text, line, field):
        """Return specific field from line in raw text."""
        results = text.split('\n')[line]
        return ' '.join(results.split()).split(' ')[field]

    def __str__(self):
        """Return CSV of results."""
        if self.test == 'STREAM':
            test_type = 'Send'
        elif self.test == 'MAERTS':
            test_type = 'Receive'
        elif self.test == 'RR':
            test_type = 'RR'

        return '%s,%s,%s,%s,%s' % (self.name, self.date, self.protocol,
                                   test_type, self.result)
