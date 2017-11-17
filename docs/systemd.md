# systemd
systemd-analyze is utilized in order to evaluate boot time for a node. It comes with a variety of sub-commands that are useful for analyzing system boot time performance. A breakdown of each subcommand is detailed below.

Of course, the use of systemd-analyze requires that systemd is used as the init system, which is not the case for Ubuntu 14.04 (Trusty). Therefore, only Ubuntu 16.04 (Xenial) and newer versions of Ubuntu get this type of testing.


## systemd-analyze
### time
The time subcommand is the default output of systemd-analyze. The output gives the breakdown of how long the kernel before userspace has been reached noted by "(kernel)" and then the time the normal system userspace took to initialize noted by "(userspace)". The stop time is when all system services have been spawned, not necessarily when they fully finished.

```
$ systemd-analyze time
Startup finished in 3.505s (kernel) + 8.524s (userspace) = 12.029s
```

Do note that the output can vary. For example, on a baremetal system there is also additional information like time spent in firmware and by the loader (e.g. grub):

```
$ systemd-analyze time
Startup finished in 14.889s (firmware) + 3.670s (loader) + 1.854s (kernel) + 21.734s (userspace) = 42.148s
```

### blame
Blame prints out a list of all running units, ordered by the time they took to initialize. Keep in mind that one service may have a much longer running time because it depended on or waited for another service to start.

Note that this output can be many dozens of lines longs:

```
$ systemd-analyze blame | head -n 10
          3.385s console-setup.service
          2.774s cloud-init-local.service
          2.743s apparmor.service
          2.160s dev-xvda1.device
          2.159s cloud-config.service
          1.501s pollinate.service
           974ms cloud-init.service
           778ms lvm2-monitor.service
           607ms networking.service
           484ms cloud-final.service
```


### critical chain
Critical chain prints a tree of the time-critical chain of units. As described in the output itself the value after the '@' symbol is the actual time during boot that the service is started. While the total time the unit took to start is printed after the '+' symbol.

Again the output might be misleading due to one service depending on another.

```
$ systemd-analyze critical-chain
The time after the unit is active or started is printed after the "@" character.
The time the unit takes to start is printed after the "+" character.

graphical.target @7.374s
└─multi-user.target @7.367s
  └─ssh.service @7.340s +21ms
    └─basic.target @5.780s
      └─sockets.target @5.772s
        └─snapd.socket @5.710s +23ms
          └─sysinit.target @5.649s
            └─cloud-init.service @4.650s +974ms
              └─networking.service @4.036s +607ms
                └─network-pre.target @3.971s
                  └─cloud-init-local.service @742ms +2.774s
                    └─systemd-remount-fs.service @333ms +291ms
                      └─systemd-journald.socket @325ms
                        └─-.slice @170ms
```

## Test Case
Here is the typical process for collecting systemd-analyze information:

1. Collect values from the above commands. Store as 'initial' times.
2. Reboot
3. After cloud-init has completed running. Store as 'reboot' times.

## Data Collection
This reboot times should be collected for a minimum of 4-5 iterations, the more the better, and the mean, median, and standard deviation calculated for each part of the reported boot time (e.g. kernel, userpsace, and total).

## Analysis
Looking for the mean and median to be in close proximity to one another. What is close is left to the reader and involves looking through the results to determine if there was no or a single outlier versus wide ranging values.

Ideally, the standard deviation should be very small, less than 1 in most cases.
