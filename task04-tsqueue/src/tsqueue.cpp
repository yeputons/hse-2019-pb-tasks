#include <cassert>
#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
	assert(q);
	queue_init(&q->q_);
	pthread_mutex_init(&q->mutex, nullptr);
	pthread_cond_init(&q->cond, nullptr);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
	assert(q);
	pthread_cond_destroy(&q->cond);
	pthread_mutex_destroy(&q->mutex);
	queue_destroy(&q->q_);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
	assert(q);
	pthread_mutex_lock(&q->mutex);
	queue_push(&q->q_, data);
	pthread_cond_signal(&q->cond);
	pthread_mutex_unlock(&q->mutex);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
	pthread_mutex_lock(&q->mutex);
	bool not_empty = !queue_empty(&q->q_);
	if (not_empty) {
		*data = queue_pop(&q->q_);
	}
	pthread_mutex_unlock(&q->mutex);
	return not_empty;
}

void* threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
	// TODO(2)
	static_cast<void>(q);  // Как-нибудь используем переменную.
	return nullptr;
}
