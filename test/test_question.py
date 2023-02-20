from plugins.xsales.Xsales import preguntas
import questionary



def test_preguntas():
    question=questionary.prompt
    d=preguntas('Server', questionari=question)
    assert d == list()

