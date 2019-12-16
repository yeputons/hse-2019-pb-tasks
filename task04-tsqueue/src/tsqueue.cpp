#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&(q->q));
    pthread_mutex_init(&(q->mutex_work), nullptr);
    pthread_cond_init(&(q->cond_start_working), nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&(q->cond_start_working));
    pthread_mutex_destroy(&(q->mutex_work));
    queue_destroy(&(q->q));
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&(q->mutex_work));
    queue_push(&(q->q), data);
    pthread_mutex_unlock(&(q->mutex_work));
    pthread_cond_signal(&q->cond_start_working);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    bool success = false;
    pthread_mutex_lock(&q->mutex_work);
    if (!queue_empty(&q->q)) {
        *data = queue_pop(&q->q);
        success = true;
    }
    pthread_mutex_unlock(&q->mutex_work);
    return success;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->mutex_work);
    while (queue_empty(&q->q)) {
        pthread_cond_wait(&q->cond_start_working, &q->mutex_work);
    }
    void *data;
    data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex_work);

    return data;
}
