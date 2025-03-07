# Stock-OA
The goal of this project was to create a real-time stock trading engine that would support stock buying and stock selling.

The data structure chosen to manage these stock orders was a linked list, since it would support frequent insertions and deletions in our list efficiently. The list used to track buy orders is sorted by our highest price while the list used to track sell orders is sorted by our lowest price.

For our function match_order(), we are able to maintain an O(N) runtime by utilizing the sorted nature of these lists to yield the two orders whose conditions we want to check.
