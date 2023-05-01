#include "Merge.h"
#include "Ours.h"

#include "../template/DPDK.h"

#define MYSKETCH Univ_Ours

std::atomic<bool> is_used[NUM_RX_QUEUE + 1];

long printing_threshold;

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
            sketch->local(i, printing_threshold);
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

int main(int argc, char **argv)
{
    int ret = main_dpdk(argc, argv);
    argc -= ret;
    argv += ret;

    printing_threshold = atol(argv[1]);

    MYSKETCH* sketch = new MYSKETCH();
    ret = rte_eal_mp_remote_launch(distribute, sketch, CALL_MAIN);

    return ret;
}
