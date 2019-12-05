#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    // TODO mutex
    queue_init(&q->q);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    // TODO mutex
    queue_destroy(&q->q);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    // TODO mutex
    queue_push(&q->q, data);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    // TODO mutex
    if(queue_empty(&q->q))
        return false;
    else { // void *queue_pop(Queue *q);
        *data = queue_pop(&q->q);
        return true;
    }
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    // TODO(2)
    static_cast<void>(q);  // Как-нибудь используем переменную.
    return nullptr;
}
