# 環境変数設定クラス
def constant_text(request):
    return {
        'APP_NAME': 'sakurazaka46rss',
    }
    
def getValue(key):
    # 引数を渡さないとエラーになるため、とりあえず空文字を渡しておく
    dict = constant_text('');
    return dict.get(key, '');