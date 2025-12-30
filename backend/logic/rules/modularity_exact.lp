% ==============================================================================
% MODULARITY MAXIMIZATION (Exact)
% ==============================================================================
% This program finds the partition that maximizes modularity Q.
% Note: This is computationally expensive (NP-Hard). Suitable for small graphs (N < 50).
% Requires pre-calculated modularity weights B_ij.

% Input:
% mod_weight(N1, N2, W): The modularity contribution if N1 and N2 are in the same community.
% node(N): Nodes in the graph.
% k: Max number of communities allowed (optional, or dynamic).

#const k=4. % Max communities to search for (heuristic limit for speed)

% ------------------------------------------------------------------------------
% 1. Generator
% ------------------------------------------------------------------------------
% Assign each node to exactly one community ID from 1..k
{ community(N, C) : C=1..k } = 1 :- node(N).

% ------------------------------------------------------------------------------
% 2. Optimization
% ------------------------------------------------------------------------------
% Maximize the sum of mod_weight for all pairs (N1, N2) that are in the same community.
% B_ij is symmetric, so we can sum just N1 < N2 or all pairs.
% Usually B_ij facts are generated for all pairs or lower triangle.
% Assuming mod_weight is given for pairs.

#maximize { W, N1, N2 : community(N1, C), community(N2, C), mod_weight(N1, N2, W) }.

% ------------------------------------------------------------------------------
% 3. Symmetry Breaking (Optional but recommended for speed)
% ------------------------------------------------------------------------------
% Force community IDs to be used in order? (Complex, skipping for now)

#show community/2.
