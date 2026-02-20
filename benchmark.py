def benchmark_storage(E, N, U, Eq, Nq, Uq):

    float_bytes = E.nbytes + N.nbytes + U.nbytes
    int_bytes = Eq.nbytes + Nq.nbytes + Uq.nbytes

    reduction = 100 * (1 - int_bytes / float_bytes)

    print("\n=== Storage Benchmark ===")
    print("Float64 size (bytes):", float_bytes)
    print("Int32 size (bytes):", int_bytes)
    print("Reduction (%):", reduction)

"""
Provides the difference between GCQT and normal storage benchmark
"""