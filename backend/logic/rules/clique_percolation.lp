% ==============================================================================
% CLIQUE PERCOLATION ALGORITHM (CPA)
% Implementation in ASP (Clingo)
% ==============================================================================

#const k = 3. % Size of cliques to percolate

% 1. Find all k-cliques
% A clique is a set of k nodes where every pair is connected.
is_clique(S) :- 
    #count { N : in_clique(N, S) } = k,
    S = #min { N : in_clique(N, S) }. % Representative ID for the set? 
    % Actually, finding all sets of size k is easier with a bitmask or set approach.
    % In Clingo, we can use a predicate for members.

{ clique_member(C, N) : node(N) } = k :- clique(C).
:- clique(C), clique_member(C, N1), clique_member(C, N2), N1 < N2, not edge(N1, N2), not edge(N2, N1).

% Generate cliques (this is a generator, might be slow if not constrained)
clique(1..100). % Upper bound on number of cliques to find
:- clique(C), not { clique_member(C, _) } = k. % Each clique ID must have k nodes
:- clique(C1), clique(C2), C1 < C2, { clique_member(C1, N) : clique_member(C2, N) } = k. % Unique cliques

% 2. Adjacency of cliques
% Two k-cliques are adjacent if they share k-1 nodes.
adjacent_cliques(C1, C2) :-
    clique(C1), clique(C2), C1 < C2,
    #count { N : clique_member(C1, N), clique_member(C2, N) } = k-1.

% 3. Communities are connected components of cliques
community_clique(C, C) :- clique(C).
community_clique(C1, C1_Rep) :- adjacent_cliques(C1, C2), community_clique(C2, C1_Rep).
community_clique(C2, C1_Rep) :- adjacent_cliques(C1, C2), community_clique(C1, C1_Rep).

% Map nodes to communities
% A node belongs to a community if it is part of any clique in that community.
community(N, CommID) :- clique_member(C, N), community_clique(C, CommID).

#show community/2.
