import MeCab
from collections import Counter

def jnoun(text):
    # MeCabのインスタンスを生成
    mecab = MeCab.Tagger('-Ochasen')
    mecab.parse('')
    node = mecab.parseToNode(text)
    
    # テキストを形態素解析し、名詞の頻度をカウントするリストを初期化
    node_list = []
    
    # ストップワードを抜く処理
    with open('./Japanese_stop_words.txt', 'r', encoding='utf-8') as f:
        stop_words = [word.strip() for word in f.readlines()]

    # 空白文字を含む要素を取り除く
    stop_words = [word for word in stop_words if word]
        
    # テキストを形態素解析
    node = mecab.parseToNode(text)
    while node:
        features = node.feature.split(',')
        if node.surface in ['「', '#','＃','」','［＃「','＃「']:
            pass  # 特定の記号や文字を無視する
        else:
            node_list.append((node.surface, features))

        node = node.next

    # stop_wordsに含まれている要素をnode_listから削除
    node_list = [word for word in node_list if word[0] not in stop_words]
    
    total_nouns = sum(1 for word in node_list if '名詞' in word[1])

    nouns = [word[0] for word in node_list if '名詞' in word[1]]
    
    top30_noun_counts = top30_jnoun(nouns)
    
    # top30_noun_countsに含まれる名詞の頻度の合計を求める
    total_top30_noun_counts = sum(count for word, count in top30_noun_counts)

    # 合計を総形態素数で割ってパーセンテージを求める
    return total_top30_noun_counts / total_nouns

def top30_jnoun(nouns):
    # 名詞の出現頻度をカウント
    noun_counts = Counter(nouns)

    # 上位30件の名詞とその頻度を取得
    top30_jnoun = noun_counts.most_common(30)

    return top30_jnoun

# ファイルからテキストを読み込む例
with open('wagahaiwa_nekodearu_utf8.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# top30_nounsが含まれる名詞の頻度を求め、上位30を表示
print(jnoun(text))
