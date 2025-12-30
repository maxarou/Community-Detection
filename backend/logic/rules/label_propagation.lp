% ==============================================================================
% LABEL PROPAGATION ALGORITHM (LPA)
% Fixed Version
% ==============================================================================

#const max_steps = 5.
step(1..max_steps).

% 1. Initialization
label(N, N, 0) :- node(N).

% 2. Count labels in neighborhood from previous step
% n_count(Node, Label, Count, Step)
n_count(N, L, C, T) :- 
    node(N), 
    step(T),
    label(M, L, T-1), 
    edge(N, M),
    C = #count { M2 : edge(N, M2), label(M2, L, T-1) }.

% 3. Find max count for each node at current step
max_n_count(N, K, T) :- 
    node(N), 
    step(T),
    K = #max { C : n_count(N, _, C, T) }.

% Handle nodes with no active neighbors (e.g. isolated) -> Keep previous label?
% If max_n_count fails (empty set), the node might die?
% Add default:
has_neighbor(N) :- edge(N, _).
label(N, L, T) :- node(N), step(T), not has_neighbor(N), label(N, L, T-1).

% 4. Identify candidate labels (those with max count)
candidate(N, L, T) :-
    n_count(N, L, K, T),
    max_n_count(N, K, T).

% 5. Select best label (lexicographically smallest to break ties)
label(N, L, T) :- 
    node(N), 
    step(T),
    has_neighbor(N),
    L = #min { X : candidate(N, X, T) }.

% Output
community(N, L) :- label(N, L, max_steps).

#show community/2.
