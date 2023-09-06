# AutoMATA (Auto Massively Parallel Thought Agent system)

![automata](https://github.com/sudy-super/AutoMATA/assets/128252727/14e00e91-e0ef-43f2-b679-3240f16e0c03)


LLMに能動的推論と疑似意識を実装するツール

[English ver.](https://github.com/sudy-super/AutoMATA/blob/main/README_en.md)

# クイックスタート

1. レポジトリをクローン
```
git clone https://github.com/sudy-super/AutoMATA.git
```

2. 該当ディレクトリに移動

```
cd AutoMATA
```

3. 依存ライブラリをインストール

```
pip install -r requirements.txt
```

4. call_llm.pyの6行目にOpenAI APIキーを入力

5. 実行

```
python main.py
```

# アーキテクチャ

**全体アーキテクチャ**

![スクリーンショット (254)](https://github.com/sudy-super/AutoMATA/assets/128252727/c36f314b-a722-476a-a257-52378204c53e)


**仮説作成/修正・行動生成モジュール**

![スクリーンショット (255)](https://github.com/sudy-super/AutoMATA/assets/128252727/78c8dd9f-c0c6-4aa3-943b-b63ed1e184f2)


# 動作例

![スクリーンショット (263)](https://github.com/sudy-super/AutoMATA/assets/128252727/10d0c4a6-fd82-4c0f-b156-83483cf80133)


# TODO

□応答のパース構造の改良

□複数のLLMで議決を取る機能を排した軽量モードの実装

□ワーキングメモリ(過去の経験の蓄積)を参照する機能の実装

□脳内会議メンバーにPaLM2, LLaMA2-70bの追加

□マルチモーダル対応
