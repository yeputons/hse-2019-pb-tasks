#include "tsqueue.h"
#include "queue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    pthread_mutex_init(&q->mutex, nullptr);
    pthread_cond_init(&q->new_element, nullptr);
    queue_init(&q->q);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    queue_destroy(&q->q);
    pthread_cond_destroy(&q->new_element);
    pthread_mutex_destroy(&q->mutex);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->new_element);
    pthread_mutex_unlock(&q->mutex);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->mutex);
    bool is_not_empty = false;
    if (!queue_empty(&q->q)) {
        is_not_empty = true;
        *data = queue_pop(&q->q);
    }
    pthread_mutex_unlock(&q->mutex);
    return is_not_empty;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->mutex);
    while (queue_empty(&q->q)) {
        pthread_cond_wait(&q->new_element, &q->mutex);
    }
    void *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);
    return data;
}
