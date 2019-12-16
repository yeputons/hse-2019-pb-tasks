#include "tsqueue.h"
#include <assert.h>
#include "queue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    assert(q);

    queue_init(&q->q);
    pthread_mutex_init(&q->mutex, nullptr);
    pthread_cond_init(&q->cond_empty, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    assert(q);

    pthread_cond_destroy(&q->cond_empty);
    pthread_mutex_init(&q->mutex, nullptr);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    assert(q);

    pthread_mutex_lock(&q->mutex);
    queue_push(&q->q, data);
    pthread_cond_signal(&q->cond_empty);
    pthread_mutex_unlock(&q->mutex);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    assert(q);

    pthread_mutex_lock(&q->mutex);
    if (queue_empty(&q->q)) {
        pthread_mutex_unlock(&q->mutex);
        return false;
    } else {
        *data = queue_pop(&q->q);  // UB if data == nullptr
    }
    pthread_mutex_unlock(&q->mutex);
    return true;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    assert(q);

    pthread_mutex_lock(&q->mutex);
    while (queue_empty(&q->q)) {
        pthread_cond_wait(&q->cond_empty, &q->mutex);
    }
    void *ans = queue_pop(&q->q);
    pthread_mutex_unlock(&q->mutex);

    return ans;
}
