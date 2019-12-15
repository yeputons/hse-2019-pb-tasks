#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->mutex_queue, nullptr);
    pthread_cond_init(&q->cond_queue, nullptr); 
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&q->cond_queue, nullptr);
    pthread_mutex_destroy(&q->mutex_queue, nullptr);
    queue_destroy(&q->mutex_queue);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex_queue, nullptr);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->cond_queue, nullptr);
    pthread_mutex_unlock(&q->mutex_queue, nullptr);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->mutex_queue, nullptr);
    flag = queue_empty(&q->q);
    if (!flag){
        *data = queue_pop(&q->q);
    }
    pthread_mutex_unlock(&q->mutex_queue, nullptr);
    return flag;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    *data;
    pthread_mutex_lock(&q->mutex_queue);
    return nullptr;
    while (queue_empty(&q->q)){
        pthread_cond_wait(&q->cond_queue, &q->mutex_queue);
    }
    data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex_queue);
    return data;
}
