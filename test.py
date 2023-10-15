def gugu(a: int) -> None:
    for i in range(1, 9+1):
        ans = a * i
        print(f"{a=} {i=} = {ans=}")
def main() -> None:
    gugu(5)
if __name__ == "__main__":
    main()
