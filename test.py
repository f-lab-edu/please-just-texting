def Gugu(a: int) -> None:
    for i in range(1, 9 + 1):
        ans = a * i
        print(f"{a=} {i=} {ans=}")


def Main() -> None:
    Gugu(2)


if __name__ == "__main__":
    Main()
