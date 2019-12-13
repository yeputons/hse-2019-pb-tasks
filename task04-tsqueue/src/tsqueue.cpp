#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    pthread_mutex_init(&(q->m), NULL);
    queue_init(&q->q);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_mutex_destroy(&(q->m)); 
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&(q->m));
    queue_push(&q->q, data);
    pthread_mutex_unlock(&(q->m));
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&(q->m));
    bool cond = false;
    if (!queue_empty(&q->q)) {
        *data = queue_pop(&q->q);
        cond = true;
    }
    pthread_mutex_unlock(&(q->m));
    return cond;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    // TODO(2)
    static_cast<void>(q);  // Как-нибудь используем переменную.
    return nullptr;
}
