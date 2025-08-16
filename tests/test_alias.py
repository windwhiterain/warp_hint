from warp_hint.alias import resolve
from warp_hint.real_generic import Generic


class List[t](Generic): ...


class Dict[k, v](Generic): ...

type A = float
type B = A

type C = List[float]
type D = C

type E[t] = float
type F[t] = E[t]

type G[t] = List[t]
type H[t] = G[t]

type I[t] = t
type J[t] = I[t]

type K[k, v] = Dict[k, v]
type L[k, v] = K[k, v]

type M[k, v] = Dict[k, v]
type N[k] = K[k, float]

type O[t] = List[t]
type P[t] = List[O[t]]

type Q[t] = List[t]
type R[t] = Q[List[t]]

type S[t] = List[t]
type T[t] = S[List[t]]
type U[t] = S[T[t]]


def test_resolve_alias():
    assert resolve(B) is float
    assert resolve(D) is List[float]
    assert resolve(F[int]) is float
    assert resolve(H[int]) is List[int]
    assert resolve(J[int]) is int
    assert resolve(L[int, str]) is Dict[int, str]
    assert resolve(N[int]) is Dict[int, float]
    assert resolve(R[int]) is List[List[int]]
    assert resolve(U[int]) is List[List[List[int]]]


if __name__ == "__main__":
    test_resolve_alias()
