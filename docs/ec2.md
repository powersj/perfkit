# ec2

EC2 has a variety of [instance types](https://aws.amazon.com/ec2/instance-types/) centered around various computing purposes. There are three areas to understand for each instance:

First, learning what [instance types](https://aws.amazon.com/ec2/instance-types/) is under test as each type has special features (e.g. faster networking, additional NVMe storage) it may contain.

Next, knowing then what the expected network performance is. Network performance is generally outlined in the [instance types](https://aws.amazon.com/ec2/instance-types/) page. Keeping in mind that all new instance types use jumbo frame size MTU of 9001.

Finally, understanding the storage credits and IOPS allowed. Storage performance depends on the type of storage, number of credits, and number of devices. Testing the [EBS volume](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonEBS.html) will require generating some files for FIO to play with, while avoiding running out of space given the small size. Whereas additional devices can be directly tested with FIO and achieve much greater IOPS. Reading the documentation for [storage optimized](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/storage-optimized-instances.html) instances is helpful for understanding peak IOPS.
