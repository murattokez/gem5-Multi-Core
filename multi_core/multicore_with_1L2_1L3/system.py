import os
import m5
from m5.objects import *
from Caches import *

import argparse
"""Adding parameters to your script
"""
from optparse import OptionParser
# Add the common scripts to our path
m5.util.addToPath('$HOME/gem5/configs')

from common import SimpleOpts


thispath = os.path.dirname(os.path.realpath(__file__))
default_binary = os.path.join(
    '$HOME/gem5/tests/test-progs/hello/bin/riscv/linux/hello')


parser = argparse.ArgumentParser()

# Binary to execute
parser.add_argument("--binary", nargs="?", default=default_binary,type=str)
parser.add_argument("-o", "--options", default="",
                        help="""The options to pass to the binary, use " "
                              around the entire string""")

# Finalize the arguments and grab the args so we can pass it on to our objects
args=parser.parse_args()

system=System(cache_line_size=128);

#set clock frekansı
system.clk_domain = SrcClockDomain()
system.clk_domain.clock='5GHz'
system.clk_domain.voltage_domain=VoltageDomain()

# Set up the system
system.mem_mode = 'timing'               # Use timing accesses
system.mem_ranges = [AddrRange('512MB')] # Create an address range

#create o3 cpu
system.cpu = [DerivO3CPU() for i in range(4)]

# Adding our caches to this system
for i in range(4):
    system.cpu[i].icache = L1ICache()
    system.cpu[i].dcache = L1DCache()
    system.cpu[i].icache.connectCPU(system.cpu[i])
    system.cpu[i].dcache.connectCPU(system.cpu[i])

# connecting the caches to our CPU ports

    """system.cpu[0].icache.connectCPU(system.cpu[0])
    system.cpu[0].dcache.connectCPU(system.cpu[0])

    system.cpu[1].icache.connectCPU(system.cpu[1])
    system.cpu[1].dcache.connectCPU(system.cpu[1])

    system.cpu[2].icache.connectCPU(system.cpu[2])
    system.cpu[2].dcache.connectCPU(system.cpu[2])

    system.cpu[3].icache.connectCPU(system.cpu[3])
    system.cpu[3].dcache.connectCPU(system.cpu[3])"""


# We can't directly connect the L1 caches to the L2 cache since the L2 cache only expects a single port to connect to it.
# Therefore, we need to create an L2 bus toconnect out L1 caches to the L2 cache. Then we can use our helper function to connect the L1 caches to the L2 bus.
system.l2bus = L2XBar()
system.l3bus = L2XBar()

# Hook the CPU ports up to the l2bus
for i in range(4):
    system.cpu[i].icache.connectBus(system.l2bus)
    system.cpu[i].dcache.connectBus(system.l2bus)

# create our two l2 cache and connect it to the L2 bus
system.l2cache1 = L2Cache()
#system.l2cache2 = L2Cache()

system.l2cache1.connectCPUSideBus(system.l2bus)
#system.l2cache2.connectCPUSideBus(system.l2bus)

# create out l3 cache and connect it to the L3 bus and the memory bus
system.l3cache = L3Cache()
system.l3cache.connectCPUSideBus(system.l3bus)


#CPU'ların bellekteki verilere erişmesini ve bellekteki verileri işlemesini sağlar.
system.membus=SystemXBar()

# Connect the L2 cache to l3bus
system.l2cache1.connectMemSideBus(system.l3bus)
#system.l2cache2.connectMemSideBus(system.l3bus)
# Connect the L3 cache to the membus
system.l3cache.connectMemSideBus(system.membus)



#interrupt controller
for i in range(4):
    system.cpu[i].createInterruptController()

# Create a DDR3 memory controller and connect it to the membus
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Connect the system up to the membus
system.system_port = system.membus.cpu_side_ports

#########################################################################

pargs = []



if args.options != "":
    pargs = args.options.split(';')

idx=0 #multiprocess operasonla icin indeximizi kullanırız bir fon dongusuyle arttırabiliriz fakat bu scrpitte single process kullanacagız

process = Process()
#process.executable = wrkld

process.cmd = [args.binary] + pargs[idx].split()
# Set the cpu to use the process as its workload and create thread contexts

system.cpu[0].workload = process
system.cpu[0].createThreads()

system.cpu[1].workload = process
system.cpu[1].createThreads()

system.cpu[2].workload = process
system.cpu[2].createThreads()

system.cpu[3].workload = process
system.cpu[3].createThreads()


system.workload = SEWorkload.init_compatible(args.binary)

# set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))
