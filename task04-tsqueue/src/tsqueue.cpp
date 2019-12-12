#include "tsqueue.h"
#include <assert.h>
#include "queue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
    queue_init(&q->q);
    pthread_mutex_init(&q->base_mutex, NULL);
    pthread_cond_init(&q->pop_cond, NULL);
    q->pop_cond_bool = 0;
    q->waiting_threads_count = 0;
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
    assert(!q->waiting_threads_count);
    queue_destroy(&q->q);
    pthread_mutex_destroy(&q->base_mutex);
    pthread_cond_destroy(&q->pop_cond);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
    pthread_mutex_lock(&q->base_mutex);
    queue_push(&q->q, data);
    if (q->waiting_threads_count) {
        q->pop_cond_bool = 1;
        pthread_cond_signal(&q->pop_cond);
    }
    pthread_mutex_unlock(&q->base_mutex);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
    pthread_mutex_lock(&q->base_mutex);
    bool is_empty = queue_empty(&q->q);
    if (!is_empty) {
        (*data) = queue_pop(&q->q);
    }
    pthread_mutex_unlock(&q->base_mutex);
    return !is_empty;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
    pthread_mutex_lock(&q->base_mutex);
    bool queue_was_empty = 0;
    if (queue_empty(&q->q)) {
        q->waiting_threads_count++;
        queue_was_empty = 1;
    }

    while (queue_empty(&q->q)) {
        q->pop_cond_bool = 0;
        while (!q->pop_cond_bool) {
            pthread_cond_wait(&q->pop_cond, &q->base_mutex);
        }
        q->pop_cond_bool = 0;
    }

    void *data_to_return = queue_pop(&q->q);

    if (queue_was_empty) {
        q->waiting_threads_count--;
    }

    pthread_mutex_unlock(&q->base_mutex);
    return data_to_return;
}
