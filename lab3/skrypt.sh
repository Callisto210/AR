for size in 3000 5000 7000 9000 11000 13000 15000 17000 19000 21000
do
	python generator.py $size > input.txt
	cat input.txt | ./seq >> results.txt

	for cpus in {2..8}
	do
		mpiexec -np $cpus ./first $size >> results.txt
	done

	for cpus in {2..8}
	do
		mpiexec -np $cpus ./second $size >> results.txt
	done
done
