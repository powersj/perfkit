# mdadm

## Array Creation
When using mdadm to create RAID arrays do the following to create a RAID 0 array with 8 devices using /dev/nvme[1-8]n1. Adjust the raid-device count and devices as necessary:

```
sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=8 /dev/nvme[1-8]n1
sudo mdadm --detail /dev/md0
```

## Speeding up Creation
If creating a more complex RAID type, like 10, the creation can take a significant amount of time. To help this tune the kernel to increase the speed limit with:

```
$ sudo sysctl -w dev.raid.speed_limit_min=50000
dev.raid.speed_limit_min = 50000
$ sudo sysctl -w dev.raid.speed_limit_max=5000000
dev.raid.speed_limit_max = 5000000
```
