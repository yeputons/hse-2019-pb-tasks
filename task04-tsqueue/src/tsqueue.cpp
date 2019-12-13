#include "tsqueue.h"
#include <cassert>

void threadsafe_queue_init(ThreadsafeQueue *q) {
    assert(q);
    queue_init(&q->q);
    pthread_mutex_init(&q->mtx, nullptr);
    pthread_cond_init(&q->cnd, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    assert(q);
    assert(queue_empty(&q->q));
    queue_destroy(&q->q);
    pthread_cond_destroy(&q->cnd);
    pthread_mutex_destroy(&q->mtx);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    assert(q);
    pthread_mutex_lock(&q->mtx);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->cnd);
    pthread_mutex_unlock(&q->mtx);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    assert(q);
    if (queue_empty(&q->q))
        return false;
    pthread_mutex_lock(&q->mtx);
    *data = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mtx);
    return true;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    assert(q);
    void *ans = 0;
    pthread_mutex_lock(&q->mtx);
    while (queue_empty(&q->q)) {
        pthread_cond_wait(&q->cnd, &q->mtx);
    }
    ans = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mtx);
    return ans;
}
