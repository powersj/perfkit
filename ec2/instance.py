"""Generic EC2 Instance class."""


class Ec2Instance(object):
    """Generic EC2 Instance class."""

    def __init__(self, instance):
        """Init class."""
        self.instance_id = instance.id
        self.type = instance.instance_type
        self.state = instance.state['Name']
        self.ami = instance.image.id
        self.ip_public = instance.public_ip_address
        self.ip_private = instance.private_ip_address
        self.owner = self._determine_owner(instance.tags)

    @staticmethod
    def _determine_owner(tags):
        """Determine owner of the instance based on tags."""
        if not tags:
            return ''

        owner = ''
        for tag in tags:
            if tag['Key'] == 'Owner':
                owner = tag['Value']

        return owner

    def __str__(self):
        """Table format."""
        return('%s %s %s %s %s %s %s' %
               (self.instance_id, self.type, self.state, self.ami,
                self.ip_public, self.ip_private, self.owner))

    def to_csv(self):
        """Object as valid csv string."""
        return('%s,%s,%s,%s,%s,%s,%s' %
               (self.instance_id, self.type, self.state, self.ami,
                self.ip_public, self.ip_private, self.owner))

    def to_json(self):
        """Object as json-like object to be used with json.dumps."""
        return {
            "id": self.instance_id,
            "type": self.type,
            "state": self.state,
            "ami": self.ami,
            "ip_public": self.ip_public,
            "ip_private": self.ip_private,
            "owner": self.owner
        }
