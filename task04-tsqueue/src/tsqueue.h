#ifndef TSQUEUE_H_
#define TSQUEUE_H_

#include <pthread.h>
#include "queue.h"

extern "C" {

struct ThreadsafeQueue {
    Queue q;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
};

void threadsafe_queue_init(ThreadsafeQueue *q);
void threadsafe_queue_destroy(ThreadsafeQueue *q);
void threadsafe_queue_push(ThreadsafeQueue *q, void *data);
bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data);
void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q);
}

#endif
