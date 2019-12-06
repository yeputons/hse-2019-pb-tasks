#include "tsqueue.h"
#include "queue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    pthread_mutex_init(&q->mutex, nullptr);
    queue_init(&q->q);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_mutex_destroy(&q->mutex);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->mutex);
    queue_push(&q->q, data);
    pthread_mutex_unlock(&q->mutex);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->mutex);
    bool is_empty = false;
    if (queue_empty(&q->q) == false) {
        is_empty = true;
        *(data) = queue_pop(&q->q);
    }
    pthread_mutex_unlock(&q->mutex);
    return is_empty;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    // TODO(2)
    static_cast<void>(q);  // Как-нибудь используем переменную.
    return nullptr;
}
