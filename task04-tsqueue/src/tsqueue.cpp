#include <assert.h>
#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&(q->q));
    assert(pthread_mutex_init(&(q->mutex), NULL) == 0);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    queue_destroy(&(q->q));
    pthread_mutex_destroy(&(q->mutex));
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&(q->mutex));   
    queue_push(&(q->q), data);
    pthread_mutex_unlock(&(q->mutex));
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&(q->mutex));   
    bool rv = !queue_empty(&(q->q));

    if (rv)
        *data = queue_pop(&(q->q));
    pthread_mutex_unlock(&(q->mutex));
    
    return rv;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    // TODO(2)
    static_cast<void>(q);  // Как-нибудь используем переменную.
    return nullptr;
}
