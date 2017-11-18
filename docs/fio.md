# fio
[fio](https://github.com/axboe/fio) or the "Flexible I/O Tester" is a widely used storage testing tool. It can spawn a variety of threads or processes to do a particular type of I/O action. The action can be against a specific device or it can create files and indirectly use those to test a device.

## Test Cases
Ideally the goal is to obtain maximum IOPS from the device under test under the following conditions:

* Sequential write
* Sequential read
* Random write
* Random read

### Common Global Options
For testing the following global options are used throughout all testing:

```
# To avoid writing to memory or cache, go directly to the storage device
direct=1
# Use the Linux native asynchronous I/O engine
ioengine=libaio
# Number of I/Os to submit at once
iodepth_batch=16
# This defines how many pieces of IO to retrieve at once
iodepth_batch_complete=16
# Enable time based tests instead of reading or writing a specified amount
time_based=1
# Ramp up for 60 seconds, before measuring
ramp_time=60
# Run for 600 seconds, 10 minutes after ramp up time
runtime=600
# Per group reports instead of per job when numjobs is specified
group_reporting=1
```

## Data Collection
Tests are run using a test case file:

```
fio <test_case>.ini -output=test.json -output-format=json
```

The resulting test.json file produces output with a couple interesting values:

1. Overall IOPS
2. Disk Utilization

The submit latency (slat) and completion latency (clat) are harder to evaluate in a cloud setting and not something that is guaranteed.

The output itself looks like the following:

```
{
  "fio version" : "fio-2.2.10",
  "timestamp" : 1510963172,
  "time" : "Fri Nov 17 23:59:32 2017",
  "jobs" : [
    {
      "jobname" : "test",
      "groupid" : 0,
      "error" : 0,
      "eta" : 0,
      "elapsed" : 661,
      "read" : {
        "io_bytes" : 0,
        "bw" : 0,
        "iops" : 0.00,
        "runtime" : 0,
        "total_ios" : 0,
        "short_ios" : 0,
        "drop_ios" : 0,
        "slat" : {
          "min" : 0,
          "max" : 0,
          "mean" : 0.00,
          "stddev" : 0.00
        },
        "clat" : {
          "min" : 0,
          "max" : 0,
          "mean" : 0.00,
          "stddev" : 0.00,
          "percentile" : {
            "1.000000" : 0,
            "5.000000" : 0,
            "10.000000" : 0,
            "20.000000" : 0,
            "30.000000" : 0,
            "40.000000" : 0,
            "50.000000" : 0,
            "60.000000" : 0,
            "70.000000" : 0,
            "80.000000" : 0,
            "90.000000" : 0,
            "95.000000" : 0,
            "99.000000" : 0,
            "99.500000" : 0,
            "99.900000" : 0,
            "99.950000" : 0,
            "99.990000" : 0,
            "0.00" : 0,
            "0.00" : 0,
            "0.00" : 0
          }
        },
        "lat" : {
          "min" : 0,
          "max" : 0,
          "mean" : 0.00,
          "stddev" : 0.00
        },
        "bw_min" : 0,
        "bw_max" : 0,
        "bw_agg" : 0.00,
        "bw_mean" : 0.00,
        "bw_dev" : 0.00
      },
      "write" : {
        "io_bytes" : 37500272,
        "bw" : 62499,
        "iops" : 15624.70,
        "runtime" : 600008,
        "total_ios" : 9374944,
        "short_ios" : 0,
        "drop_ios" : 0,
        "slat" : {
          "min" : 17,
          "max" : 9602,
          "mean" : 32.18,
          "stddev" : 48.61
        },
        "clat" : {
          "min" : 964,
          "max" : 261110,
          "mean" : 8151.19,
          "stddev" : 3262.83,
          "percentile" : {
            "1.000000" : 1752,
            "5.000000" : 7968,
            "10.000000" : 8032,
            "20.000000" : 8096,
            "30.000000" : 8096,
            "40.000000" : 8160,
            "50.000000" : 8160,
            "60.000000" : 8160,
            "70.000000" : 8256,
            "80.000000" : 8256,
            "90.000000" : 8256,
            "95.000000" : 8256,
            "99.000000" : 8640,
            "99.500000" : 9536,
            "99.900000" : 14912,
            "99.950000" : 112128,
            "99.990000" : 150528,
            "0.00" : 0,
            "0.00" : 0,
            "0.00" : 0
          }
        },
        "lat" : {
          "min" : 989,
          "max" : 261142,
          "mean" : 8182.26,
          "stddev" : 3262.73
        },
        "bw_min" : 1,
        "bw_max" : 23552,
        "bw_agg" : 25.02,
        "bw_mean" : 15639.50,
        "bw_dev" : 770.29
      },
      "trim" : {
        "io_bytes" : 0,
        "bw" : 0,
        "iops" : 0.00,
        "runtime" : 0,
        "total_ios" : 0,
        "short_ios" : 0,
        "drop_ios" : 0,
        "slat" : {
          "min" : 0,
          "max" : 0,
          "mean" : 0.00,
          "stddev" : 0.00
        },
        "clat" : {
          "min" : 0,
          "max" : 0,
          "mean" : 0.00,
          "stddev" : 0.00,
          "percentile" : {
            "1.000000" : 0,
            "5.000000" : 0,
            "10.000000" : 0,
            "20.000000" : 0,
            "30.000000" : 0,
            "40.000000" : 0,
            "50.000000" : 0,
            "60.000000" : 0,
            "70.000000" : 0,
            "80.000000" : 0,
            "90.000000" : 0,
            "95.000000" : 0,
            "99.000000" : 0,
            "99.500000" : 0,
            "99.900000" : 0,
            "99.950000" : 0,
            "99.990000" : 0,
            "0.00" : 0,
            "0.00" : 0,
            "0.00" : 0
          }
        },
        "lat" : {
          "min" : 0,
          "max" : 0,
          "mean" : 0.00,
          "stddev" : 0.00
        },
        "bw_min" : 0,
        "bw_max" : 0,
        "bw_agg" : 0.00,
        "bw_mean" : 0.00,
        "bw_dev" : 0.00
      },
      "usr_cpu" : 0.41,
      "sys_cpu" : 1.05,
      "ctx" : 647600,
      "majf" : 0,
      "minf" : 44,
      "iodepth_level" : {
        "1" : 0.00,
        "2" : 0.00,
        "4" : 0.00,
        "8" : 0.00,
        "16" : 0.10,
        "32" : 110.16,
        ">=64" : 0.00
      },
      "latency_us" : {
        "2" : 0.00,
        "4" : 0.00,
        "10" : 0.00,
        "20" : 0.00,
        "50" : 0.00,
        "100" : 0.00,
        "250" : 0.00,
        "500" : 0.00,
        "750" : 0.00,
        "1000" : 0.01
      },
      "latency_ms" : {
        "2" : 1.08,
        "4" : 0.13,
        "10" : 98.39,
        "20" : 0.32,
        "50" : 0.01,
        "100" : 0.00,
        "250" : 0.06,
        "500" : 0.01,
        "750" : 0.00,
        "1000" : 0.00,
        "2000" : 0.00,
        ">=2000" : 0.00
      },
      "latency_depth" : 32,
      "latency_target" : 0,
      "latency_percentile" : 100.00,
      "latency_window" : 0
    }
  ],
  "disk_util" : [
    {
      "name" : "xvda",
      "read_ios" : 0,
      "write_ios" : 645585,
      "read_merges" : 0,
      "write_merges" : 9682645,
      "read_ticks" : 0,
      "write_ticks" : 5269136,
      "in_queue" : 5269148,
      "util" : 100.00
    }
  ]
}
```

## Analysis
The goal, similar to networking, is to achieve the advertised maximum IOPS and to verify you can consistently achieve those IOPS. Of course, note that some clouds give instances a certain number of IOPS allowed over a certain period of time. Therefore, being aware of these limitations or testing on fresh instances is strongly desired.
