import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="h1", value="This is a Header", props={"href":"www.msn.com"})
        node2 = HTMLNode(tag="h1", value="This is a Header", props={"href":"www.msn.com"})
        self.assertEqual(node.__repr__(), node2.__repr__())

    def test_constructor(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html(self):
        node_empty_props = HTMLNode(props={})
        node_multiple_props = HTMLNode(props={"key1": "abc", "key2": "xyz"})
        node_weird_props = HTMLNode(props={"*&^%/32fas": "prop_value"})
        self.assertEqual(node_empty_props.props_to_html(), "")
        self.assertEqual(node_multiple_props.props_to_html(), ' key1="abc" key2="xyz"')
        self.assertEqual(node_weird_props.props_to_html(), ' *&^%/32fas="prop_value"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_value(self):
        node = LeafNode(tag="h1", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_tag(self):
        node = LeafNode(tag=None, value="This is some text")
        self.assertEqual(node.to_html(), node.value)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_multiple_children(self):
        child_node = LeafNode("span", "child")
        child2_node = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node, child2_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><p>child2</p></div>")

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_nested_parent(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        grandparent_node = ParentNode("h1", [parent_node])
        self.assertEqual(
            grandparent_node.to_html(),
            "<h1><div><span>child</span></div></h1>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span></div>')


if __name__ == "__main__":
    unittest.main()