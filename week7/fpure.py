def f(n:int) -> int:
  def g(a:int,c:int) -> int:
    if n > a:
        return g(a*2+1, c+1)
    else:
        return c
  return g(0,-1)