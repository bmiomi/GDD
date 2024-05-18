from unittest import TestCase, main

from plugins.xsales.confi import Config

class TestConfig(TestCase):
    
    def setUp(self) -> None:
        self.config=Config()
        
    def test_preguntas(self):
        value={'s':'s'}
        self.assertEqual(type(value),dict)

if __name__=="__main__":
    main()


