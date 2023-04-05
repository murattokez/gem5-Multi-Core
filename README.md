# gem5-Multi-Core

4 different system designs for cache analysis. [Ligra](https://github.com/jshun/ligra) benchmark used as test binary. First, ligra must be modified for gem5 and for RISC-V. If the changes made in Ligra are to be explained, the ligra.h file has been updated with the addition of a parameter named "num_cpu" to obtain information about how many CPUs the system will be simulated with. You can see the added code below:

```
int num cpu = P.getOptionIntValue("-n",1);
setWorkers(num cpu);
```
The benchmarks of Ligra have been compiled with RISC-V gcc. Some parameters are required to compile programs that use OPENMP in gcc. Sample steps used for a benchmark are shared below.

```
riscv64-unknown-linux-gnu-gcc -static -fopenmp -DOPENMP -Wall -O0 -I. -c
BFS.C -o BFS.o

riscv64-unknown-linux-gnu-g++ -static -DOPENMP -L. -o BFS BFS.o -lgomp -
lpthread -ldl

```
Commands have been written individually for each benchmark and the corresponding RISC-V binary files have been obtained. 

To start the simulation and get the results:

```
bash run_multicore.sh
```
