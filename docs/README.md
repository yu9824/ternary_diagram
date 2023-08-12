# ドキュメント作成手順

## sphinxのプロジェクトを作成

```bash
sphinx-quickstart docs
```

ディレクトリを分けるか、という質問にはyesと答える。

## docstringから.rstを生成

```bash
sphinx-apidoc -f -o docs/source ./ternary_diagram
```

