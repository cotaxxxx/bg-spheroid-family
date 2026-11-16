# 実装への差し戻し（第 4 回）：S1 R4 の動作検査の結果

対象：S1 R4（zip の SHA-256 `72de77a659db01d48fbcefcbf53c8d7f715a629aade0e21240c52ad3b5091155`）

この差し戻しは、研究用 PC での動作検査と、あなたのコード・導出だけに基づいている。ほかの資料の式や数値は含まない。

## 1. 動作検査の結果

`producer.jl 47/10 47/10 s1_ledger.tsv 4 4` を流したところ、次のエラーで止まった。

```text
MethodError: reducing over an empty collection is not allowed; consider supplying `init` to the reducer
```

台帳が作られなかったため、checker も `s1_ledger.tsv` が見つからずに止まった。

## 2. 原因（`producer.jl` の `aseries_derivative`）

**(a) 空の積（今回のエラー）**

```julia
factor=coeff*prod(BigInt(k-j) for j in 0:d-1)*...
```

d ＝ 0 のとき、`0:d-1` が空になる。`prod(...; init=BigInt(1))` のように、空のときの値を与えること。

**(b) d ＝ 0 のときの冪の始まり（数学の誤り。(a) を直すと表に出ずに値が間違う）**

d ＝ 0 のとき `power=x` から始めている。そのため、ループの k ＝ 1 で先に `power=power*x` が行われ、x² から足し始めることになる。つまり、Σ a_k x^k ではなく、Σ a_k x^(k+1) を計算してしまう。d ＝ 0 でも、`power` は 1 から始めること（d ≥ 1 の場合と同じ扱い）。

直したあとは、次を自分で確かめること。

- d ＝ 0、1、2 のそれぞれで、k ＝ 1、2、3 の項が a_k x^k、−k a_k x^(k−1)、k(k−1) a_k x^(k−2) になっているか。
- 小さな点の入力（たとえば x ＝ 1/10 の定数の jet）で、A、A′、A″ の値が、あなたの導出の式と合うか。

## 3. 返してほしいもの

- 直した新しい版（R4 の原本は変更しないこと）
- 変更点の一覧
- SHA-256 の一覧

入力は、これまでどおり pack V2、契約、差し戻しだけとする。
