#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->mutex_queue, nullptr);
    pthread_cond_init(&q->cond_queue, nullptr); 
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&q->cond_queue);
    pthread_mutex_destroy(&q->mutex_queue);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex_queue);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->cond_queue);
    pthread_mutex_unlock(&q->mutex_queue);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->mutex_queue);
    bool is_empty = queue_empty(&q->q);
    if (!is_empty) {
        *data = queue_pop(&q->q);
    }
    pthread_mutex_unlock(&q->mutex_queue);
    return is_empty;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->mutex_queue);
    while (queue_empty(&q->q)){
        pthread_cond_wait(&q->cond_queue, &q->mutex_queue);
    }
    void * data;
    data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex_queue);
    return data;
}
