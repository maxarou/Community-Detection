% ==============================================================================
% SCHEMA DEFINITION
% ==============================================================================

% Predicate: node(ID)
% Represents a node in the graph.
% ID: The unique identifier of the node (integer or symbol).

% Predicate: edge(Source, Target)
% Represents a directed edge from Source to Target.
% For undirected graphs, we typically generate symmetric facts or symmetric rules.

% Predicate: weight(Source, Target, W)
% Optional weight for the edge. Default is 1.

% Predicate: community(Node, Label)
% Assigns a Node to a community identified by Label.

#show node/1.
#show edge/2.
#show community/2.
