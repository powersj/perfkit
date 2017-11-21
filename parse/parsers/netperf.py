"""Parse netperf results."""


class Netperf(object):
    """Netperf Parsing Object."""

    def __init__(self, log_path):
        """Collect relevant information."""
        name = log_path.split('/')[-1].split('-')[0]
        self.protocol = name.split('_')[0]
        self.test = name.split('_')[1]
        self.date = log_path.split('/')[-1].split('-')[1].replace('.log', '')

        with open(log_path) as f:
            lines = f.read()

        if self.test == 'RR':
            self.result = self._get_request_response(lines)
        elif self.protocol == 'UDP':
            self.result = self._get_udp_throughput(lines)
        else:
            self.result = self._get_tcp_throughput(lines)

    def _get_request_response(self, lines):
        """Parse request and response output."""
        results = lines.split('\n')[-3]
        return ' '.join(results.split()).split(' ')[5]

    def _get_udp_throughput(self, lines):
        """Parse UDP stream output."""
        results = lines.split('\n')[-4]
        return ' '.join(results.split()).split(' ')[5]

    def _get_tcp_throughput(self, lines):
        """Parse TCP stream output."""
        results = lines.split('\n')[-2]
        return ' '.join(results.split()).split(' ')[4]

    def __str__(self):
        """Return CSV of results."""
        if self.test == 'STREAM':
            name = 'Send'
        elif self.test == 'MAERTS':
            name = 'Receive'
        elif self.test == 'RR':
            name = 'RR'

        return '%s,%s,%s,%s' % (self.date, self.protocol, name, self.result)
