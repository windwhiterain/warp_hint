from warp_hint.alias import resolve_alias

type A = float
type B = A

type C = list[float]
type D = C

type E[t] = float
type F[t] = E[t]

type G[t] = list[t]
type H[t] = G[t]

type I[t] = t
type J[t] = I[t]

type K[k, v] = dict[k, v]
type L[k, v] = K[k, v]

type M[k, v] = dict[k, v]
type N[k] = K[k, float]

type O[t] = list[t]
type P[t] = list[O[t]]

type Q[t] = list[t]
type R[t] = Q[list[t]]

type S[t] = list[t]
type T[t] = S[list[t]]
type U[t] = S[T[t]]


def test_resolve_alias():
    assert resolve_alias(B) is float
    assert resolve_alias(D) == list[float]
    assert resolve_alias(F[int]) is float
    assert resolve_alias(H[int]) == list[int]
    assert resolve_alias(J[int]) is int
    assert resolve_alias(L[int, str]) == dict[int, str]
    assert resolve_alias(N[int]) == dict[int, float]
    assert resolve_alias(R[int]) == list[list[int]]
    assert resolve_alias(U[int]) == list[list[list[int]]]

