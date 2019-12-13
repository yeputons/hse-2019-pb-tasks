#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->mutex_que, nullptr);
    pthread_cond_init(&q->cond_que, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_cond_destroy(&q->cond_que);
    pthread_mutex_destroy(&q->mutex_que);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex_que);
    queue_push(&q->q, data);
    pthread_mutex_unlock(&q->mutex_que);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->mutex_que);
    bool flag = false;
    *data = nullptr;
    if (!queue_empty(&q->q)) {
        *data = queue_pop(&q->q);
        flag = true;
    }
    pthread_mutex_unlock(&q->mutex_que);
    return flag;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    // TODO(2) NONONO
    static_cast<void>(q);  // Как-нибудь используем переменную.
    return nullptr;
}
