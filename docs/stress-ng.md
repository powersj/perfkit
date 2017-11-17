# stress-ng
Utilize stress-ng to collect the 'bogo ops' of the system. Bogo ops are "bogus operations per second" a measure of throughput. As described in the stress-ng manual, they give a rough notion of performance, but are not an accurate benchmarking figure and certainly not be to treated with any seriousness.

## Test Case
The below command will launch the test on all CPUs for 10 minutes and produce the time summary.

```
$ stress-ng --matrix 0 --timeout 10m --metrics-brief --times
stress-ng: info:  [4399] dispatching hogs: 72 matrix
stress-ng: info:  [4399] successful run completed in 600.05s (10 mins, 0.05 secs)
stress-ng: info:  [4399] stressor      bogo ops real time  usr time  sys time   bogo ops/s   bogo ops/s
stress-ng: info:  [4399]                          (secs)    (secs)    (secs)   (real time) (usr+sys time)
stress-ng: info:  [4399] matrix        99686236    600.00  43196.82      0.00    166143.74      2307.72
stress-ng: info:  [4399] for a 600.05s run time:
stress-ng: info:  [4399]   43203.94s available CPU time
stress-ng: info:  [4399]   43197.18s user time   ( 99.98%)
stress-ng: info:  [4399]       0.01s system time (  0.00%)
stress-ng: info:  [4399]   43197.19s total time  ( 99.98%)
stress-ng: info:  [4399] load average: 72.16 62.48 34.37
```

## Data Collection
The number that is most interesting from the above output is the "bogo ops/s (real time)" rate. This value is the total bogo ops measured divided by the total run time.

## Analysis
Looking for this value to be consistent across runs (e.g. low standard deviation) and relatively similar between releases.
