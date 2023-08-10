#include "Merge.h"
#include "Ours.h"

#include "../template/DPDK.h"

#define MYSKETCH Univ_Ours
#define CHILDSKETCH_TYPE MyChild_Univ

std::atomic<bool> is_used[NUM_RX_QUEUE + 1];

int distribute(void *arg){
    MYSKETCH* sketch = (MYSKETCH*) arg;

    if(rte_get_main_lcore() == rte_lcore_id()){
        print_stats();
        return 1;
    }

    bool set = true;

    set = is_used[0].exchange(set);
    if(!set){
        sketch->coordinator(NUM_RX_QUEUE);
        return 2;
    }

    for(uint32_t i = 0;i < NUM_RX_QUEUE;++i){
        set = is_used[i + 1].exchange(set);
        if(!set){
            sketch->local(i, &(child_sketches[i]));
            return 3;
        }
    }

    RTE_LOG(INFO, L2FWD, "nothing to do for lcore %u\n", rte_lcore_id());

    return 0;
}

weak_atomic<int32_t> Univ_Ours::PROMASK{0x8};

void print_parameters() {
    printf("Sketch parameters\n%d %d %d %d\n", MAX_LEVEL, HASH_NUM, LENGTH, HEAP_SIZE);
}

void print_sketch_counters_2(void* sketch) {
    CHILDSKETCH_TYPE* child_sketch = (CHILDSKETCH_TYPE*)sketch;

    for(uint32_t i = 0; i < MAX_LEVEL; i++) {
        for(uint32_t j = 0; j < HASH_NUM; j++) {
            for(uint32_t k = 0; k < LENGTH; k++) {
                if(child_sketch->sketch[i][j][k] != 0) {
                    printf("Counter: %" Value_printf_specifier" %d %d %d\n", child_sketch->sketch[i][j][k], i, j, k);
                }
            }
        }
    }
    printf("Finished printing counters\n");
    
    for(uint32_t i = 0; i < MAX_LEVEL; i++) {
        printf("Packet count: %d %"PRIu64"\n", i, child_sketch->packet_count[i]);
    }

    fflush(stdout);
}

int main(int argc, char **argv)
{
    int ret = main_dpdk(argc, argv);
    argc -= ret;
    argv += ret;

    print_parameters();

    MYSKETCH* sketch = new MYSKETCH();
    ret = rte_eal_mp_remote_launch(distribute, sketch, CALL_MAIN);

    return ret;
}
