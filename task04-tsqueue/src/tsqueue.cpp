#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->mutex, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_mutex_destroy(&q->mutex);
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    // TODO
    static_cast<void>(q);  // Как-нибудь используем переменную.
    static_cast<void>(data);  // Как-нибудь используем переменную.
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    // TODO
    static_cast<void>(q);
    static_cast<void>(data);
    return false;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    // TODO(2)
    static_cast<void>(q);  // Как-нибудь используем переменную.
    return nullptr;
}
