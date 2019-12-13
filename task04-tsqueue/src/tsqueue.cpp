#include "tsqueue.h"
#include <cassert>

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    assert(pthread_cond_init(&q->cond_flag_changed, nullptr) == 0);
    assert(pthread_mutex_init(&(q->mutex), NULL) == 0);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    queue_destroy(&q->q);
    pthread_cond_destroy(&(q->cond_flag_changed));
    pthread_mutex_destroy(&q->mutex);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex);

    queue_push(&q->q, data);

    pthread_cond_signal(&q->cond_flag_changed);
    pthread_mutex_unlock(&q->mutex);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->mutex);

    bool not_empty = !queue_empty(&q->q);
    if (not_empty)
        *data = queue_pop(&q->q);

    pthread_mutex_unlock(&q->mutex);
    return not_empty;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->mutex);

    while (queue_empty(&q->q))
        pthread_cond_wait(&q->cond_flag_changed, &q->mutex);

    void *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);

    return data;
}
