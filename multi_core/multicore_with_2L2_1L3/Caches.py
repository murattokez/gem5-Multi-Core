import m5

from m5.objects import Cache



# This BaseCache will serve as the framework for our chache structure
# Underneath the hood, these python abstractions will be passed to the C++ implementation of the object

# here we will be extending a BaseCache object provided to us by creating caches with specified parameters
class L1Cache(Cache):
    """Simple L1 Cache with default values"""

    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    

   
    def connectBus(self, bus):
        """Connect this cache to a memory-side bus"""
        self.mem_side = bus.cpu_side_ports

    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU-side port
           This must be defined in a subclass"""
        raise NotImplementedError

# extensions of L1 cache: i and d cache
class L1ICache(L1Cache):
    """Simple L1 instruction cache with default values"""

   
    size = '32kB'


    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU icache port"""
        self.cpu_side = cpu.icache_port

class L1DCache(L1Cache):
    """Simple L1 data cache with default values"""

    
    size = '32kB'

    
    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU dcache port"""
        self.cpu_side = cpu.dcache_port


# Now we create an L2 cache with reasonable attributes
class L2Cache(Cache):
    """Simple L2 Cache with default values"""

    # Default parameters
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports


# Now we create an L3 cache with reasonable attributes
class L3Cache(Cache):
        size = '2048kB' # Much bigger than L2
        assoc=16
	    
        tag_latency=15

        data_latency = 20 # Latency for the return path on a miss
        response_latency = 0
        
        mshrs= 60
        tgts_per_mshr = 16 # Max number of access per MSHR

        def connectCPUSideBus(self, bus):
                """Connect this cache to a cpu-side bus"""
                self.cpu_side = bus.master
        def connectMemSideBus(self, bus):
                """Connect this cache to a memory-side bus"""
                self.mem_side = bus.slave