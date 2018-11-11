for size in {16, 16, 32, 64, 128, 256, 512, 1024}
do
	for cpus in {1..8}
	do
		mpiexec -np $cpus ./main $size >> results.txt
	done
done
