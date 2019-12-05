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
    QueueNode *node = (QueueNode *)(malloc(sizeof(QueueNode)));
    node->data = data;
    node->next = nullptr;
    if ((q->q).last) {
        (q->q).last->next = node;
    } else {
        (q->q).head = node;
    }
    (q->q).last = node;
    pthread_mutex_unlock(&q->m);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->m);
    bool attempt;
    QueueNode *node = (q->q).head;
    if (node != nullptr) {
        *data = node->data;
        (q->q).head = node->next;
        if (!(q->q).head)
            (q->q).last = nullptr;
        attempt = true;
        free(node);
    } else
        attempt = false;
    pthread_mutex_unlock(&q->m);
    return attempt;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    // TODO(2)
    static_cast<void>(q);  // Как-нибудь используем переменную.
    return nullptr;
}
