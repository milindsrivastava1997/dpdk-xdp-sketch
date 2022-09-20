#ifndef LOCHER_MERGE_H
#define LOCHER_MERGE_H

#include "config.h"
#include "template/Merge.h"

template<uint32_t thread_num>
class Locher_Merge : public Merge<Packet, MyLocher*, thread_num>{
public:

    typedef ReaderWriterQueue<MyLocher*> myQueue;

    Sketch<Packet>* initialize_parent(){
        return new MyLocher();
    }

    Sketch<Packet>* initialize_child(){
        return initialize_parent();
    }

    Sketch<Packet>* insert_child(Sketch<Packet>* p, myQueue& q, const Packet& packet, uint32_t number, uint32_t thread_id){
        p->insert_one(packet);

        if((number % (INTERVAL * thread_num)) == (INTERVAL * thread_id)){
            q.enqueue((MyLocher*)p);
            return initialize_child();
        }
        return p;
    }

    void merge(Sketch<Packet>* p, MyLocher* temp){
        ((MyLocher*)p)->Merge(temp);
    }
};

#endif
