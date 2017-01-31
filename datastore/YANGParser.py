from rest_framework.parsers import BaseParser
from pyang import Context
from pyang import FileRepository
from pyang import yang_parser
from rest_framework.parsers import ParseError


class YANGParser(BaseParser):
    media_type = 'application/yang'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Check the syntactic validity of the model
        """
        yang_model = stream.read().decode('utf-8')
        ctx = Context(FileRepository())
        ctx.add_module('yang', yang_model, format='yang')
        parser = yang_parser.YangParser()
        res = parser.parse(ctx, 'yang', yang_model)
        if res is None:
            raise ParseError(detail="yang not valid")
        return yang_model.encode('utf-8')
