# netperf
[Netperf](https://github.com/HewlettPackard/netperf) is a benchmark to measure various areas of network performance. It is used to collect bulk data transfer in a single direction or request/response performance of a network device.

It runs by having one system run the netserver to act as the target and the other system to run netperf against the server.

## Options
Netperf has a very large number of test options that can be very useful in additional data collection Here is a summary of what is used:

* -c Local CPU utilization and service calculations
* -C Remote CPU utilization and service calculations
* -n # Specify the number of CPUs in the system
* -D # Display interim results every # seconds
* -f [m|g] Display throughput in megabits or gigabits (Stream only)

## Test Cases
To gain a sense of basic performance of the network device the following is collected over an IPv4 address using whatever the default MTU is:

* TCP Send (tcp_stream)
* TCP Receive (tcp_maerts)
* UDP Send (udp_stream)
* TCP Request/Response (tcp_rr)
* UDP Request/Response (udp_rr)

TCP Stream tests result in output like the following:

```
Recv   Send    Send                          Utilization       Service Demand
Socket Socket  Message  Elapsed              Send     Recv     Send    Recv
Size   Size    Size     Time     Throughput  local    remote   local   remote
bytes  bytes   bytes    secs.    10^6bits/s  % S      % S      us/KB   us/KB

 87380  16384  16384    600.00     10039.11   0.54     0.87     0.320   0.514
```

UDP stream tests also include throughput, but add in error counts as well:

```
Socket  Message  Elapsed      Messages                   CPU      Service
Size    Size     Time         Okay Errors   Throughput   Util     Demand
bytes   bytes    secs            #      #   10^6bits/sec % SS     us/KB

212992   65507   600.00    26022634      0    22728.8     0.92     0.240
212992           600.00        128               0.1     0.00     0.001
```

Request/response results produce the following:

```
Local /Remote
Socket Size   Request Resp.  Elapsed Trans.   CPU    CPU    S.dem   S.dem
Send   Recv   Size    Size   Time    Rate     local  remote local   remote
bytes  bytes  bytes   bytes  secs.   per sec  % S    % S    us/Tr   us/Tr

16384  87380  1       1      600.00  16941.71  0.19   0.19   7.881   8.053
16384  87380
```

## Data Collection
In the case of the stream tests the throughput, normally in megabits or gigabits per second, is more interesting. Then calculating the mean over all runs of those values.

For request/response tests the transfers per second value is most important. Collecting this data and calculating the mean over the various runs is the most important.

## Analysis
Looking to achieve the advertise network speed of the device. Low outliers or being unable to achieve the advertised speed are red flags.
