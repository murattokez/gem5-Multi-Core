multicore_scripts=('multicore_with_2L2_1L3' 'multicore_with_1L2_0L3' 'multicore_with_1L2_1L3' 'multicore_with_4L2_1L3')
ligra_benchmarks=('BC' 'BFS' 'BFS-Bitvector' 'BFSCC' 'CF' 'Components' 'KCore' 'MIS' 'PageRank' 'PageRankDelta' 'Radii' 'Triangle')

for multicore_scripts in "${multicore_scripts[@]}"; do
	for ligra_benchmarks in "${ligra_benchmarks[@]}"; do
		$HOME/gem5/build/RISCV/gem5.opt -d $HOME/gem5/m5out/ligra_multicore/${ligra_benchmarks}_riscv/${multicore_scripts}_${ligra_benchmarks}_riscv \
		--stats-file=${multicore_scripts}_${ligra_benchmarks}_riscv.txt --dump-config=${multicore_scripts}_${ligra_benchmarks}_riscv.ini \
		$HOME/gem5/configs/multi_core/$multicore_scripts/system.py --binary=$HOME/ligra/apps/riscv_binaries/$ligra_benchmarks -o "-n 4 $HOME/ligra/inputs/rMatGraph_J_5_100"
	done
done
		
		
for multicore_scripts in "${multicore_scripts[@]}"; do
	
		$HOME/gem5/build/RISCV/gem5.opt -d $HOME/gem5/m5out/ligra_multicore/BellmanFord_riscv/${multicore_scripts}_BellmanFord_riscv \
		--stats-file=${multicore_scripts}_BellmanFord_riscv.txt --dump-config=${multicore_scripts}_BellmanFord_riscv.ini \
		$HOME/gem5/configs/multi_core/$multicore_scripts/system.py --binary=$HOME/ligra/apps/riscv_binaries/BellmanFord -o "-n 4 $HOME/ligra/inputs/rMatGraph_WJ_5_100"
	
done
