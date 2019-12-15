#include "tsqueue.h"
#include <assert.h>

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    assert(pthread_mutex_init(&q->mutex, nullptr) == 0);
    assert(pthread_cond_init(&q->cond_push, nullptr) == 0);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&q->cond_push);
    pthread_mutex_destroy(&q->mutex);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->cond_push);
    pthread_mutex_unlock(&q->mutex);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->mutex);
    if (queue_empty(&q->q)) {
        pthread_mutex_unlock(&q->mutex);
        return false;
    }
    *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);
    return true;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->mutex);
    while (queue_empty(&q->q))
        pthread_cond_wait(&q->cond_push, &q->mutex);
    void *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);
    return data;
}
