#ifndef PRINT_UTIL_H
#define PRINT_UTIL_H

typedef uint64_t padded_sketch_t;

void print_counters_once() {
    print_stats_once();
    ncpus = libbpf_num_possible_cpus();
    padded_sketch_t* sketch_ptr = new padded_sketch_t [ncpus];
    Value sketch_ptr_sum = 0;
    int ret;

    memset(sketch_ptr, 0, sizeof(padded_sketch_t) * ncpus);

    for (uint32_t sketch_idx = 0; sketch_idx < LENGTH * HASH_NUM; sketch_idx++) {
        ret = bpf_map_lookup_elem(global_sketch_fd, &sketch_idx, sketch_ptr);
        if(ret < 0) {
            printf("sketch fd ret: %d dbg: %d\n", ret, sketch_idx);
        }
        for (uint32_t i = 0; i < ncpus; i++) {
            sketch_ptr_sum += sketch_ptr[i];
        }
        if(sketch_ptr_sum != 0) {
            printf("Counter: %" Value_printf_specifier" %d\n", sketch_ptr_sum, sketch_idx);
        }
        sketch_ptr_sum = 0;
    }
    printf("Finished printing counters\n");
    fflush(stdout);
    fprintf(stderr, "Finished printing counters\n");

    delete [] sketch_ptr;
}

void sigint_handler(int signum) {
    printf("Got sigint\n");
    print_counters_once();
    exit(0);
}

#endif
