#include "tsqueue.h"

void threadsafe_queue_init(ThreadsafeQueue *q) {
  // TODO
  pthread_mutex_init(&q->m, NULL);
  queue_init(&q->q);
}

void threadsafe_queue_destroy(ThreadsafeQueue *q) {
  // TODO
  queue_destroy(&q->q);
  pthread_mutex_destroy(&q->m);
}

void threadsafe_queue_push(ThreadsafeQueue *q, void *data) {
  // TODO
  pthread_mutex_lock(&q->m);
  queue_push(&q->q, data);
  pthread_mutex_unlock(&q->m);
}

bool threadsafe_queue_try_pop(ThreadsafeQueue *q, void **data) {
  // TODO
  pthread_mutex_lock(&q->m);
  if (queue_empty(&q->q)) {
    pthread_mutex_unlock(&q->m);
    return false;
  }
  *data = queue_pop(&q->q);
  pthread_mutex_unlock(&q->m);
  return true;
}

void *threadsafe_queue_wait_and_pop(ThreadsafeQueue *q) {
  // TODO(2)
  static_cast<void>(q); // Как-нибудь используем переменную.
  return nullptr;
}
