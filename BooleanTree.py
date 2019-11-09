from enum import Enum


class NodeType(Enum):
    AND = 1
    OR = 2
    LEAF = 3
    OPEN_BRACKET = 4
    CLOSE_BRACKET = 5
    NOT = 6


class BooleanTreeNode:
    node_type = None
    value = None
    left = None
    right = None

    def __init__(self, node_type):
        self.node_type = node_type

    def get_boolean_value(self, vid):

        if self.node_type == NodeType.AND:
            left_expression_value = self.left.get_boolean_value(vid)
            right_expression_value = self.right.get_boolean_value(vid)
            return left_expression_value and right_expression_value

        elif self.node_type == NodeType.OR:
            left_expression_value = self.left.get_boolean_value(vid)
            right_expression_value = self.right.get_boolean_value(vid)
            return left_expression_value or right_expression_value

        elif self.node_type == NodeType.NOT:
            return not self.value.get_boolean_value(vid)

        else:
            return self.value.lower() in vid.lower()


class Tokenizer:
    expression = None
    tokens = None
    tokenTypes = None
    i = 0

    def __init__(self, exp):
        self.expression = exp

    def next(self):
        self.i += 1
        return self.tokens[self.i - 1]

    def peek(self):
        return self.tokens[self.i]

    def hasNext(self):
        return self.i < len(self.tokens)

    def nextTokenType(self):
        return self.tokenTypes[self.i]

    def tokenize(self):
        if type(self.expression) != str:
            string = ""
            for term in self.expression:
                string += term + " "
            self.expression = string[:-1]
        import re
        reg = re.compile(
            r'(\bAND\b|\bAnd\b|\band\b|\bOR\b|\bOr\b|\bor\b|\bNOT\b|\bNot\b|\bnot\b| !|\(|\))')
        self.tokens = reg.split(self.expression)
        self.tokens = [t.strip() for t in self.tokens if t.strip() != '']

        self.tokenTypes = []
        for t in self.tokens:
            if t == 'AND' or t == "&&" or t == "And" or t == "and":
                self.tokenTypes.append(NodeType.AND)
            elif t == 'OR' or t == "||" or t == "or" or t == "Or":
                self.tokenTypes.append(NodeType.OR)
            elif t == '(':
                self.tokenTypes.append(NodeType.OPEN_BRACKET)
            elif t == ')':
                self.tokenTypes.append(NodeType.CLOSE_BRACKET)
            elif t == 'NOT' or t == 'Not' or t == 'not' or t == '!':
                self.tokenTypes.append(NodeType.NOT)
            else:
                # TAG
                self.tokenTypes.append(NodeType.LEAF)


class BooleanParser:
    tokenizer = None
    root = None

    def __init__(self, exp):
        self.tokenizer = Tokenizer(exp)
        self.tokenizer.tokenize()
        self.parse()

    def parse(self):
        self.root = self.parse_expression()

    def parse_expression(self):
        andTerm1 = self.parse_AND_term()
        while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == NodeType.OR:
            self.tokenizer.next()
            andTermX = self.parse_AND_term()
            andTerm = BooleanTreeNode(NodeType.OR)
            andTerm.left = andTerm1
            andTerm.right = andTermX
            andTerm1 = andTerm
        return andTerm1

    def parse_AND_term(self):
        not1 = self.parse_NOT_term()
        while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == NodeType.AND:
            self.tokenizer.next()
            notX = self.parse_NOT_term()
            condition = BooleanTreeNode(NodeType.AND)
            condition.left = not1
            condition.right = notX
            not1 = condition
        return not1

    def parse_NOT_term(self):
        if self.tokenizer.nextTokenType() == NodeType.NOT:
            if self.tokenizer.hasNext():
                self.tokenizer.next()
                expression = self.parse_condition()
                not_node = BooleanTreeNode(NodeType.NOT)
                not_node.value = expression
                return not_node
            else:
                raise Exception("NOT term expects a value next to it. No values where found")
        return self.parse_condition()



    def parse_condition(self):
        if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == NodeType.OPEN_BRACKET:
            self.tokenizer.next()
            expression = self.parse_expression()
            if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == NodeType.CLOSE_BRACKET:
                self.tokenizer.next()
                return expression
            else:
                raise Exception("Closing ) expected, but got " + self.tokenizer.next())

        terminal1 = self.parse_terminal()
        return terminal1

    def parse_terminal(self):
        if self.tokenizer.hasNext():
            tokenType = self.tokenizer.nextTokenType()
            if tokenType == NodeType.LEAF:
                n = BooleanTreeNode(tokenType)
                n.value = self.tokenizer.next()
                return n
            else:
                raise Exception('NUM, STR, or VAR expected, but got ' + self.tokenizer.next())

        else:
            raise Exception('NUM, STR, or VAR expected, but got ' + self.tokenizer.next())

    def get_boolean_value(self, vid):
        return self.root.get_boolean_value(vid)


# parser = BooleanParser("(horror and !comedy) or (romance and comedy)")
# vid = "romance/comedy/les_intouchables"
#
# print(parser.get_boolean_value(vid))
#
# vid = "romance/forgetting_sara_marshall"
#
# print(parser.get_boolean_value(vid))
#
# vid = "something_not_relevant"
# print(parser.get_boolean_value(vid))
