#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->mutex_work, nullptr);
    pthread_cond_init(&q->cond_start_cause_queue_is_not_empty, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&q->cond_start_cause_queue_is_not_empty);
    pthread_mutex_destroy(&q->mutex_work);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex_work);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->cond_start_cause_queue_is_not_empty);
    pthread_mutex_unlock(&q->mutex_work);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->mutex_work);
    bool queue_is_not_empty = !queue_empty(&q->q);
    if (queue_is_not_empty)
        *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex_work);
    return queue_is_not_empty;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->mutex_work);
    while (queue_empty(&q->q)) {
        pthread_cond_wait(&q->cond_start_cause_queue_is_not_empty,
                          &q->mutex_work);
    }
    void *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex_work);
    return data;
}
