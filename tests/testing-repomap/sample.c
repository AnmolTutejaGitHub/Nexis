#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Node {
    int value;
    struct Node *next;
};

struct Stack {
    struct Node *top;
    int size;
};

int sum_array(int *arr, int len) {
    int total = 0;
    for (int i = 0; i < len; i++) total += arr[i];
    return total;
}

void push(struct Stack *stack, int val) {
    struct Node *node = malloc(sizeof(struct Node));
    node->value = val;
    node->next = stack->top;
    stack->top = node;
    stack->size++;
}

int pop(struct Stack *stack) {
    if (!stack->top) return -1;
    struct Node *node = stack->top;
    int val = node->value;
    stack->top = node->next;
    free(node);
    stack->size--;
    return val;
}

char *repeat_str(const char *s, int n) {
    char *out = malloc(strlen(s) * n + 1);
    out[0] = '\0';
    for (int i = 0; i < n; i++) strcat(out, s);
    return out;
}
