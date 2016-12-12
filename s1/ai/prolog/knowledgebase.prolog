father(daniele, michela).
father(daniele, jacopo).
father(eriberto, michela).
father(antonio, eriberto).
mother(alma, eriberto).
mother(annamaria, daniele).
mother(annamaria, marcello).
mother(annamaria, sandro).

male(jacopo)
male(sandro)
male(antonio)
male(daniele)
male(eriberto)
male(marcello)

female(annamaria)
female(michela)
female(alma)

% rules

% returns true if X is parent of Y
son(X, Y) :- father(Y, X).
son(X, Y) :- mother(Y, X).

% X is grandfather :- X is Y father AND Y is Z father
grandFather(X, Z) :- father(X, Y)   ,   father(Y, Z).

% X and Y are s :-  Y is son of P and X is son of P, P1,P2, X!=Y, P1==P2
sibling(X, Y) :- son(Y, P1), son(X, P2), X \= Y, P1 == P2.
%...........mark P as Y's fathers, mark P as X father
sibling(X, Y) :- son(Y, P), son(X, P), X \= Y.

% P1 is X up 1, P2 is Y up 1, if P1, P2 are sibling
cousin(X, Y) :- son(X, P1), son(Y, P2), sibling(P1, P2), X \= Y.

% returns true if X is uncle or aunt of Y
% P is Y up 1, P and X are sibling
aunt_uncle(X, Y) :- son(P, Y), sibling(X, P).

% return true if X is downstream of Y
descendant(X, Y):- son(X, Y). % 1 step
descendant(X, Y):- son(Z,Y), descendant(X, Z). % if 1 step is false, recursion

% return true if X is downstream of Y
descendant2(X, Y):- son(Z,Y), descendant2(X, Z). % if 1 step is false, recursion
descendant2(X, Y):- son(X, Y). % 1 step

% return true if X and Y are males and same father
brother(X, Y):- son(X, P), son(Y, P), male(X), male(Y).

% true  if X and Y are same row
% 
sg(X, X). % X is in the same row of himself
% Z is all parrents of X, W is all sg(Z),  W is parent of Y
% parents are same generations => sons are same generation
sg(X, Y) :- parent(Z, X), sg(Z, W), parent(W, Y)