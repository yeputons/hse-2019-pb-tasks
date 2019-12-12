#include "tsqueue.h"
#include <assert.h>
#include <stdlib.h>

void threadsafe_queue_init(ThreadsafeQueue *q) {
    pthread_mutex_init(&q->m, nullptr);
    pthread_cond_init(&q->cond_push, nullptr);
    queue_init(&(q->q));
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_mutex_destroy(&q->m);
    pthread_cond_destroy(&q->cond_push);
    queue_destroy(&(q->q));
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->m);
    queue_push(&(q->q), data);
    pthread_cond_signal(&q->cond_push);
    pthread_mutex_unlock(&q->m);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->m);
    if (!queue_empty(&(q->q))) {
        *data = queue_pop(&(q->q));
        pthread_mutex_unlock(&q->m);
        return 1;
    }
    pthread_mutex_unlock(&q->m);
    return 0;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->m);
    void *data;
    if (queue_empty(&q->q)) {
        pthread_cond_wait(&q->cond_push, &q->m);
        data = queue_pop(&q->q);
    } else
        data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->m);
    return data;
}
