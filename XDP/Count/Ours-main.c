#include "../xdp_common/Abstract.h"

#include "XDP_Count.h"

#include "../../sketch/Count.h"

#define HASH_NUM 3
#define LENGTH 65536
#define HEAP_SIZE 0x3ff

#include "../xdp_common/print_util.h"

template<typename Key>
using MyCount = Count<Key, HASH_NUM, LENGTH, HEAP_SIZE>;

static uint32_t processed = 0;
static int32_t old_length = 0;
static int32_t threshold = 64;

static int32_t out_thd_fd, out_len_fd;

static MyCount<uint64_t>* p;

int handle_entry(void *ctx, void *data, size_t data_sz){
    Count_Entry<uint64_t> *e = (Count_Entry<uint64_t>*)data;
    p->Merge(*e);

    processed += 1;

    if((processed & 0x3f) == 0x3f){
        struct Length len;
        bpf_map_lookup_elem(out_len_fd, &zero, &len);

        int32_t new_length = len.length;
        int32_t gap = new_length - old_length;
        int32_t tmp_length = new_length + gap;
        int32_t new_thres = threshold;

        if(tmp_length < LOWER_LENGTH && gap < 32){
            new_thres = threshold - 1;
            new_thres = MIN(0x7e, new_thres);
            new_thres = MAX(0x3f, new_thres);
        }
        else if(tmp_length > UPPER_LENGTH && gap > -32){
            new_thres = threshold + 1;
            new_thres = MIN(0x7e, new_thres);
            new_thres = MAX(0x3f, new_thres);
        }

        if(new_thres != threshold){
            bpf_map_update_elem(out_thd_fd, &zero, &new_thres, BPF_EXIST);
        }

        threshold = new_thres;
        old_length = new_length;
    }
        
    return 0;
}

class Ours : public Abstract{
public:

    int32_t merge(){
        p = new MyCount<uint64_t>();

        out_len_fd = len_fd;
        out_thd_fd = thd_fd;

        struct ring_buffer *rb = ring_buffer__new(buf_fd, handle_entry, NULL, NULL);

        if(!rb){
            printf("Error on ring buffer\n");
            return -1;
        }

        int32_t err = 0;
        while(true){
            err = ring_buffer__consume(rb);
            if (err == -EINTR) {
                printf("EINTR\n");
                break;
            }
            if (err < 0) {
                printf("Error polling ring buffer: %d\n", err);
                break;
            }
        }

        delete p;
        return 0;
    }
    
};

void print_parameters() {
    printf("Sketch parameters\n%d %d %d\n", HASH_NUM, LENGTH, HEAP_SIZE);
}

int main(int argc, char *argv[]){
    print_parameters();
    Abstract* abs = new Ours();
    abs->update();
    delete abs;
    return 0;
}
