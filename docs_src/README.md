# ドキュメント作成手順

## sphinxのプロジェクトを作成

```bash
sphinx-quickstart docs_src
```

ディレクトリを分けるか、という質問にはnoと答える。

なお、docs内に作成しなかったのは、github-pagesがプロジェクトのrootディレクトリか、./docsディレクトリのどちらかしかhtml公開のrootにできないため。

### index.rstの改変

index.rstに`modules`を加える。

```rest
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules
```



## docstringから.rstを生成

```bash
sphinx-apidoc -f -o docs_src ./ternary_diagram --module-first --private --separate
```

## .rstからhtmlの生成

```bash
sphinx-build -b html ./docs_src ./docs
```
