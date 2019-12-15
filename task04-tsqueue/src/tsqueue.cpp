#include "tsqueue.h"
#include <cassert>

void threadsafe_queue_init(ThreadsafeQueue *q) {
		pthread_mutex_init(&q->mutex, nullptr);
		pthread_cond_init(&q->cond, nullptr);
		queue_init(&q->q);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
		assert(queue_empty(&q->q));
		pthread_mutex_destroy(&q->mutex);
		pthread_cond_destroy(&q->cond);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
		pthread_mutex_lock(&q->mutex);
		queue_push(&q->q, data);
		pthread_mutex_unlock(&q->mutex);
		pthread_cond_signal(&q->cond);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
		bool res=false;
		pthread_mutex_lock(&q->mutex);
		if(!queue_empty(&q->q))
			*data = queue_pop(&q->q), res = true;
		pthread_mutex_unlock(&q->mutex);
		return res;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
		pthread_mutex_lock(&q->mutex);
		if(queue_empty(&q->q))
				pthread_cond_wait(&q->cond, &q->mutex);
		void* res = queue_pop(&q->q);
		pthread_mutex_unlock(&q->mutex);
    return res;
}
