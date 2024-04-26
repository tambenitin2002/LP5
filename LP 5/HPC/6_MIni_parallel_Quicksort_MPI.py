from mpi4py import MPI
import numpy as np
import time

def quicksort(arr):
    """Quicksort algorithm to sort an array."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def parallel_quicksort(arr):
    """Parallel quicksort algorithm."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Scatter data
    if rank == 0:
        data_chunks = np.array_split(arr, size)
    else:
        data_chunks = None

    local_data = comm.scatter(data_chunks, root=0)

    # Perform local quicksort
    local_data = np.sort(local_data)

    # Gather sorted chunks
    sorted_data = comm.gather(local_data, root=0)

    if rank == 0:
        # Merge sorted chunks
        sorted_data = np.concatenate(sorted_data)
        return sorted_data

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        # Generate random data
        np.random.seed(42)
        data_size = 1000000  # Size of the dataset
        data = np.random.randint(1, 100, size=data_size)

        # Measure execution time for parallel quicksort
        start_time_parallel = time.time()
        sorted_data_parallel = parallel_quicksort(data)
        execution_time_parallel = time.time() - start_time_parallel
        print("Parallel Quicksort execution time:", execution_time_parallel)

        # Measure execution time for normal quicksort
        start_time_normal = time.time()
        sorted_data_normal = quicksort(data.copy())
        execution_time_normal = time.time() - start_time_normal
        print("Normal Quicksort execution time:", execution_time_normal)
    else:
        sorted_data_parallel = None
        sorted_data_normal = None

    # Broadcast sorted data
    sorted_data_parallel = comm.bcast(sorted_data_parallel, root=0)
    sorted_data_normal = comm.bcast(sorted_data_normal, root=0)

    # Optionally, print sorted data
    # print("Rank", rank, ":", sorted_data_parallel)
    # print("Rank", rank, ":", sorted_data_normal)
