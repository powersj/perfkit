# PerfKit
This is my personal collection of scripts and helpers for cloud performance testing.

## Cattle vs Pets
Because the testing I do is typically in a cloud enviornment the guidelines and for what I wish to achive is a little different than a typical system testing.

Traditional performance testing is done in a pristine enviornment with dedicated hardware or at least hardware that is well known and understood. This type of testing a la "Westminister Kennel Dog Show" is not what this is about.

This testing is looking at representative sampling of the herd. Cloud tests are run effectively in a black box enviornment. There is no knowledge of the enviornment's state in terms of noise. As such tests need to be run mulitple times on the same hardware/sizing. This avoids having noisy neighbors from standing out and affecting test results, changes to the hardware effecting test results.

## Preqs
The following is required for the scripts to work:

```
apt update
apt install -y python3-boto3 python3-paramiko
```

## Directories
### bin
These are all the scripts and tools used on the system under test (SUT). They are pushed after a sucessful launch.

### docs
The docs directory is a collection of tidbits, links, and other information I have learned along the way.

## Test Cases
* Boot
    * Initial Boot + Reboot Time
    * Values taken from systemd-analyze
    * Looking for long poll in tent and cloud-init ID time
* Storage
    * fio used to achive peak IOPS
    * Sequential 100% read and 100% write
    * Random 100% read and 100% write
    * In-cases of multiple disks, RAID 0 via mdadm is used
* Network
    * netperf is the tool of choice for single stream performance
    * TCP transmit and recieve
    * UDP transmit
    * TCP and UDP request/response
* Processor
    * stress-ng's bogomips test

## Future Items
These are tests and areas to investigate for future testing:

* Mel Gorman's MM tests
    * https://lwn.net/Articles/509577/
    * https://lwn.net/Articles/509585/

* Intel's Linux Kernel Performance:
    * https://01.org/lkp/

* Brendan Gregg:
    * http://www.brendangregg.com/linuxperf.html

* Stats Gathering
    * Use perf or sysdig for stats gathering
    * Logging stats can be an overhead
    * Run test 10 tests, get population std.dev, mean, and median
    * Stats to consider:
        * swapin/out stats
        * load rates, #number of processes running etc
        * irq rates
        * wakeup events
        * context switches
        * I/O latencies
        * thermal stats
        * cache behavour
        * syscall rates
        * blocked and I/O wait stats
        * Power consumption
            * Lots of useful CPU and memory stats in modern CPUs
            * See powerstat
