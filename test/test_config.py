from module import settings


def test_conexao_padrao():
    assert type(settings.CONEXAO_ESPELHO) == dict
    
def test_conexao_email():
    assert type(settings.CONEXAO_EMAIL) == dict
