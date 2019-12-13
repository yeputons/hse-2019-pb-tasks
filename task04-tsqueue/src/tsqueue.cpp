#include "tsqueue.h"
#include <assert.h>
#include "queue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->base_mutex, NULL);
    pthread_cond_init(&q->not_empty_cond, NULL);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&q->not_empty_cond);
    pthread_mutex_destroy(&q->base_mutex);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->base_mutex);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->not_empty_cond);
    pthread_mutex_unlock(&q->base_mutex);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->base_mutex);
    bool is_empty = queue_empty(&q->q);
    if (!is_empty) {
        *data = queue_pop(&q->q);
    }
    pthread_mutex_unlock(&q->base_mutex);
    return !is_empty;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->base_mutex);
    while (queue_empty(&q->q)) {
            pthread_cond_wait(&q->not_empty_cond, &q->base_mutex);
    }

    void *data_to_return = queue_pop(&q->q);

    pthread_mutex_unlock(&q->base_mutex);
    return data_to_return;
}
