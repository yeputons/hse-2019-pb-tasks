#include "tsqueue.h"
#include <assert.h>
#include "queue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->mutex, nullptr);
    pthread_cond_init(&q->queue_not_empty_cond, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&q->queue_not_empty_cond);
    pthread_mutex_destroy(&q->mutex);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex);  // lck -> psh -> cndtn -> nlck
    queue_push(&q->q, data);
    pthread_cond_signal(&q->queue_not_empty_cond);
    pthread_mutex_unlock(&q->mutex);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->mutex);
    bool is_empty = queue_empty(&q->q);
    if (!is_empty)
        *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);
    return !is_empty;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->mutex);
    while (queue_empty(&q->q))
        pthread_cond_wait(&q->queue_not_empty_cond, &q->mutex);
    void *return_data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);
    return return_data;
}
