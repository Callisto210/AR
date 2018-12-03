for size in 20000000 30000000 40000000 50000000 60000000 70000000
do
	./seq $size >> results.txt

	for cpus in {2..8}
	do
		mpiexec -np $cpus ./main $size >> results.txt
	done
done
