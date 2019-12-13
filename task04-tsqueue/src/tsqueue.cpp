#include "tsqueue.h"
#include <cassert>

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->mtx, nullptr);
    pthread_cond_init(&q->cnd, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    assert(queue_empty(&q->q));
    queue_destroy(&q->q);
    pthread_mutex_destroy(&q->mtx);
    pthread_cond_destroy(&q->cnd);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mtx);
    queue_push(&q->q, data);
    pthread_mutex_unlock(&q->mtx);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    if (queue_empty(&q->q))
        return false;
    pthread_mutex_lock(&q->mtx);
    *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mtx);
    return true;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    void *ans = 0;
    pthread_mutex_lock(&q->mtx);
    while (queue_empty(&q->q)) {
        pthread_cond_wait(&q->cnd, &q->mtx);
    }
    ans = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mtx);
    return ans;
}
