"""Parse FIO results."""
import json


class Fio(object):
    """FIO Parsing Object."""

    def __init__(self, log_path):
        """Store relevant information."""
        filename = log_path.split('/')[-1]

        if 'read' in filename:
            self.type = 'read'
        else:
            self.type = 'write'

        self.date = filename.split('-')[-1].replace('.json', '')

        if 'random' in filename:
            self.name = '%s-%s' % (self.type, 'random')
        else:
            self.name = self.type

        with open(log_path) as json_data:
            data = json.load(json_data)

        self.iops = data['jobs'][0][self.type]['iops']
        self.bw = data['jobs'][0][self.type]['bw']
        self.io_bytes = data['jobs'][0][self.type]['io_bytes']
        self.disk_util_mean = self._calc_disk_mean(data['disk_util'])

    def __str__(self):
        """Return CSV of results."""
        return '%s,%s,%s,%s,%s,%s' % (self.date, self.name, self.iops, self.bw,
                                      self.io_bytes, self.disk_util_mean)

    @staticmethod
    def _calc_disk_mean(disks):
        """Determine mean disk utilization."""
        total = 0.0
        for disk in disks:
            total = total + disk['util']

        return total / len(disks)
