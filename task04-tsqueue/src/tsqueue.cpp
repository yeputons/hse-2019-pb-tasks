#include "tsqueue.h"
#include "queue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    pthread_mutex_init(&q->mutex, nullptr);
    pthread_cond_init(&q->cond_empty, nullptr);
    queue_init(&q->q);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    queue_destroy(&q->q);
    pthread_mutex_destroy(&q->mutex);
    pthread_cond_destroy(&q->cond_empty);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->cond_empty);
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
    while (queue_empty(&q->q)) {
        pthread_cond_wait(&q->cond_empty, &q->mutex);
    }
    void *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);
    return data;
}
