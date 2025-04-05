class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # str representing HTML tag name (p/a/h1/etc.)
        self.value = value  # str representing value inside the tag
        self.children = children    # list of HTMLNode object children
        self.props = props  # dict of HTML tag attributes (ex: href:url)

    def to_html(self):
        '''TODO'''
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ''
        return ''.join(f' {k}="{v}"' for k,v in self.props.items())
    
    def __repr__(self):
        return f'tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props}'  
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        '''Renders a lead node as an HTML string'''
        if not self.value:
            raise ValueError("missing value")
        
        if not self.tag:
            return self.value
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag")
        
        if not self.children:
            raise ValueError("missing children")
        
        child_html = ''.join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'