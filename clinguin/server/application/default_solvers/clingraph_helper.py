clingraph_helper = """
#defined clingraph_cautious/0.
#defined clingraph_brave/0.

#show node(NODE): node(NODE), not clingraph_cautious, not clingraph_brave, show_untagged.
#show edge(EDGE): edge(EDGE), not clingraph_cautious, not clingraph_brave, show_untagged.
#show graph(GRAPH): graph(GRAPH), not clingraph_cautious, not clingraph_brave, show_untagged.
#show attr(TYPE, ID, NAME, VALUE) : attr(TYPE, ID, NAME, VALUE), not clingraph_cautious, not clingraph_brave, show_untagged.

#show node(NODE): node(NODE), clingraph_cautious, show_cautious.
#show edge(EDGE): edge(EDGE), clingraph_cautious, show_cautious.
#show graph(GRAPH): graph(GRAPH), clingraph_cautious, show_cautious.
#show attr(TYPE, ID, NAME, VALUE) : attr(TYPE, ID, NAME, VALUE),  clingraph_cautious, show_cautious.

#show node(NODE): node(NODE), clingraph_brave, show_brave.
#show edge(EDGE): edge(EDGE), clingraph_brave, show_brave.
#show graph(GRAPH): graph(GRAPH), clingraph_brave, show_brave.
#show attr(TYPE, ID, NAME, VALUE) : attr(TYPE, ID, NAME, VALUE), clingraph_brave, show_brave.

"""


