from enum import Enum


class NodeType(Enum):
    AND = 1
    OR = 2
    LEAF = 3
    OPEN_BRACKET = 4
    CLOSE_BRACKET = 5


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

        else:
            return self.value in vid


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
        reg = re.compile(r'(\bAND\b|&&|\|\||\bOR\b|\(|\))')
        self.tokens = reg.split(self.expression)
        self.tokens = [t.strip() for t in self.tokens if t.strip() != '']

        self.tokenTypes = []
        for t in self.tokens:
            if t == 'AND' or t == "&&":
                self.tokenTypes.append(NodeType.AND)
            elif t == 'OR' or t == "||":
                self.tokenTypes.append(NodeType.OR)
            elif t == '(':
                self.tokenTypes.append(NodeType.OPEN_BRACKET)
            elif t == ')':
                self.tokenTypes.append(NodeType.CLOSE_BRACKET)
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
        self.root = self.parseExpression()

    def parseExpression(self):
        andTerm1 = self.parseAndTerm()
        while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == NodeType.OR:
            self.tokenizer.next()
            andTermX = self.parseAndTerm()
            andTerm = BooleanTreeNode(NodeType.OR)
            andTerm.left = andTerm1
            andTerm.right = andTermX
            andTerm1 = andTerm
        return andTerm1

    def parseAndTerm(self):
        condition1 = self.parseCondition()
        while self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == NodeType.AND:
            self.tokenizer.next()
            conditionX = self.parseCondition()
            condition = BooleanTreeNode(NodeType.AND)
            condition.left = condition1
            condition.right = conditionX
            condition1 = condition
        return condition1

    def parseCondition(self):
        if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == NodeType.OPEN_BRACKET:
            self.tokenizer.next()
            expression = self.parseExpression()
            if self.tokenizer.hasNext() and self.tokenizer.nextTokenType() == NodeType.CLOSE_BRACKET:
                self.tokenizer.next()
                return expression
            else:
                raise Exception("Closing ) expected, but got " + self.tokenizer.next())

        terminal1 = self.parseTerminal()
        return terminal1

    def parseTerminal(self):
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


# parser = BooleanParser(["horror", "&&", "comedy"])
# vid = "comedy/horror/les_intouchables"
#
# print(parser.get_boolean_value(vid))
#
# vid = "romance/forgetting_sara_marshall"
#
# print(parser.get_boolean_value(vid))
#
# vid = "something_not_relevant"
# print(parser.get_boolean_value(vid))
