#include "tsqueue.h"
#include <assert.h>
#include <iostream>

void threadsafe_queue_init(ThreadsafeQueue *q) {
    assert(q);
    queue_init(&q->q);
    int error = pthread_mutex_init(&q->mutex, NULL);
    assert(error == 0);
    error = pthread_cond_init(&q->cv, NULL);
    assert(error == 0);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    assert(q);
    queue_destroy(&q->q);
    pthread_mutex_destroy(&q->mutex);
    pthread_cond_destroy(&q->cv);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    assert(q);
    pthread_mutex_lock(&q->mutex);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->cv);
    pthread_mutex_unlock(&q->mutex);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    assert(q);
    assert(data);
    pthread_mutex_lock(&q->mutex);
    bool is_empty = queue_empty(&q->q);
    if (!is_empty) {
        *data = queue_pop(&q->q);
    }
    pthread_mutex_unlock(&q->mutex);
    return !is_empty;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    void *result;
    pthread_mutex_lock(&q->mutex);
    while (queue_empty(&q->q)) {
        pthread_cond_wait(&q->cv, &q->mutex);
    }
    result = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);
    return result;
}