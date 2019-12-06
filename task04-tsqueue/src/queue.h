#ifndef QUEUE_H_
#define QUEUE_H_

extern "C" {

struct QueueNode;
struct Queue {
    QueueNode *head, *last;
};

void queue_init(Queue *q);
void queue_destroy(Queue *q);
bool queue_empty(Queue *q);
void queue_push(Queue *q, void *data);
void *queue_pop(Queue *q);
}

#endif