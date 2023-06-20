#ifndef XDP_PARSE_H
#define XDP_PARSE_H

#include <linux/tcp.h>
#include <linux/udp.h>
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_endian.h>

#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/in.h>

//struct Packet{
//    uint32_t src;
//    uint32_t dst;
//};

//inline void init_key(struct Packet* key, uint64_t src, uint64_t dst){
//    bpf_printk("SM: init key: %lx %lx\n", src, dst);
//    key->src = src;
//    key->dst = dst;
//    bpf_printk("SM: init key: %x %x\n", key->src, key->dst);
//}

inline void init_key(uint64_t* key, uint64_t src, uint64_t dst) {
    *key = ((src << 32) | dst);
    bpf_printk("SM: init key: %lx %x %x\n", *key, src, dst);
}

//inline int32_t parse_key(struct xdp_md *skb, struct Packet* key){
inline int32_t parse_key(struct xdp_md *skb, uint64_t* key){
    void *data_end = (void *)(long)skb->data_end;
    void *data = (void *)(unsigned long long)skb->data;
    struct iphdr *iph = data + sizeof(struct ethhdr);

    if((void*)iph + sizeof(struct iphdr) > data_end) {
        return -1;
    }
    if(iph->protocol == IPPROTO_TCP) {
        if((void*)iph + sizeof(struct iphdr) + sizeof(struct tcphdr) > data_end)
            return -1;
        struct tcphdr *h = ((void*)iph) + sizeof(struct iphdr);
        //init_key(key, h->source, h->dest);
        init_key(key, bpf_ntohl(iph->daddr), bpf_ntohs(h->dest));
        return 0;
    }
    else if(iph->protocol == IPPROTO_UDP) {
        if((void*)iph + sizeof(struct iphdr) + sizeof(struct udphdr) > data_end)
            return -1;
        struct udphdr *h = ((void*)iph) + sizeof(struct iphdr);
        //init_key(key, h->source, h->dest);
        init_key(key, bpf_ntohl(iph->daddr), bpf_ntohs(h->dest));
        return 0;
    }
    else 
        return -1;
}

#endif
