% ==============================================================================
% MODULARITY OPTIMIZATION (Exact)
% ==============================================================================
% Finds the partition that maximizes modularity Q.
% 
% The modularity Q is proportional to: Sum ( A_ij - k_i*k_j / 2m ) * delta(c_i, c_j)
% We pre-computed the weights B_ij = 2m*A_ij - k_i*k_j in 'karate_mod.lp'.
% Now we just need to maximize the sum of B_ij for all pairs in the same community.

% 1. Search Space: Assign each node to a community.
% We can limit the number of communities to K (e.g. 4 or 5) to speed up, 
% or allow up to N communities.
#const k=5. 

{ community(N, C) : C=1..k } = 1 :- node(N).

% 2. Optimization Goal
% Maximize the sum of weights for pairs (u,v) that share the same community C.
% The weights B_ij are provided by facts: mod_weight(U, V, W).
% Note: mod_weight is symmetric and likely sparse (only non-zero).

#maximize { W,U,V : community(U, C), community(V, C), mod_weight(U, V, W) }.

% 3. Symmetry Breaking (Crucial for performance)
% To avoid checking permutations of community labels (1,2 vs 2,1).
% We enforce that community ID C can only be used if C-1 is used (or similar strategy).
% Simple strategy: The community ID of node N must be <= N (if IDs were 1..N).
% Better: Canonical naming.
% Provide a basic ordering or just let Clingo solver heuristics handle it for N=34.

#show community/2.
