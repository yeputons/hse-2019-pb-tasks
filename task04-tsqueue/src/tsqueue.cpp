#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    // TODO
    queue_init(&q->q);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    // TODO
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    // TODO
    queue_push(&q->q, data);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    // TODO
    if (queue_empty(&q->q)) return false;
    *data = queue_pop(&q->q);
    return true;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    // TODO(2)
    static_cast<void>(q);  // Как-нибудь используем переменную.
    return nullptr;
}
