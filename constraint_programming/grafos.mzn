include "globals.mzn";

int: Nodes;
int: Edges;

set of int: N = 0..Nodes-1;
set of int: E = 1..Edges;

array[E] of int: n_p;
array[E] of int: n_h;
array[N] of var N : colors;
var int : mc;

constraint colors[0] = 0;
constraint forall(v in E)(colors[n_h[v]] != colors[n_p[v]]);
constraint mc = max(colors);

solve :: int_search(colors, smallest, indomain_min, complete) satisfy;