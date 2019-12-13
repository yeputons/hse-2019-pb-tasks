#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->m, nullptr);
    pthread_cond_init(&q->cond, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&q->cond);
    pthread_mutex_destroy(&q->m);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->m);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->cond);
    pthread_mutex_unlock(&q->m);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->m);
    bool can_pop = false;
    if (!queue_empty(&q->q)) {
        *data = queue_pop(&q->q);
        can_pop = true;
    }
    pthread_mutex_unlock(&q->m);
    return can_pop;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->m);
    while (queue_empty(&q->q)) {
        pthread_cond_wait(&q->cond, &q->m);
    }
    void *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->m);
    return data;
}
