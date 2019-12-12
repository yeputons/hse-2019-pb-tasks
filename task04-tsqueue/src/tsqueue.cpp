#include "tsqueue.h"
#include <assert.h>
#include <stdlib.h>

void threadsafe_queue_init(ThreadsafeQueue *q) {
    pthread_mutex_init(&q->m, nullptr);
    (q->q).head = nullptr;
    (q->q).last = nullptr;
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    pthread_mutex_destroy(&q->m);
    assert(!(q->q).head);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->m);
    queue_push(&(q->q), data);
    pthread_mutex_unlock(&q->m);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->m);
    if (!queue_empty(&(q->q))) {
        *data = queue_pop(&(q->q));
        pthread_mutex_unlock(&q->m);
        return 1;
    }
    pthread_mutex_unlock(&q->m);
    return 0;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    // TODO(2)
    static_cast<void>(q);  // Как-нибудь используем переменную.
    return nullptr;
}
