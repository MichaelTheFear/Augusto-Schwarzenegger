# run script from terminal and check exit code

import subprocess
from Genetics import Genetics
import multiprocessing
import time

# run 10 in parallel


"""
def run_script(genes):

"""

def my_function(index):
    process = subprocess.Popen(['python', "Digivolving.py",str(index)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process.kill()
    if process.returncode > 4000000000:
        return (process.returncode - 400000000) * -1
    else:
        return process.returncode

def save_best_genome(genome, score):
    with open("best_genome.txt", "a") as f:
        f.write(f"genome: {genome}\nscore: {score}\n")

def run(num_processes, start_genes):
    pool = multiprocessing.Pool(processes=num_processes)

    # Map the function to the range of indices
    results = pool.map(my_function, start_genes)

    # Close the pool of worker processes
    pool.close()
    pool.join()

    return results
    

if __name__ == '__main__':
    num_processes = 8
    genes = Genetics(num_processes)
    start_genes = genes.generate_population()

    while True:
        try:
            fitness = run(num_processes, start_genes)
            f_genes = [(start_genes[i],fitness[i]) for i in range(len(fitness))]
            m = max(f_genes)
            i = f_genes.index(m)
            print("melhor genoma ",m)
            print("index ",i)
            save_best_genome(start_genes[i], fitness[i])
            print(f"best genome: {f_genes}")
            start_genes = genes._digivolve(f_genes)
        except:
            time.sleep(30)

